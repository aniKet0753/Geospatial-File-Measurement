import json
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import BadZipFile, ZipFile

import geopandas as gpd


def process_geospatial_file(filename: str, contents: bytes) -> dict:
    extension = Path(filename).suffix.lower()

    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir) / Path(filename).name
        temp_path.write_bytes(contents)

        if extension == ".kml":
            gdf = read_kml(temp_path)
        elif extension == ".zip":
            gdf = read_shapefile_zip(temp_path, Path(temp_dir))
        else:
            raise ValueError(
                "Only KML files and ZIP archives containing Shapefiles are supported."
            )

        return calculate_measurements(gdf, filename)


def read_kml(path: Path):
    try:
        gdf = gpd.read_file(path, driver="KML")
    except Exception as exc:
        raise ValueError(f"Unable to read KML file: {exc}") from exc

    validate_gdf(gdf, "KML")
    return gdf


def read_shapefile_zip(path: Path, temp_dir: Path):
    extraction_dir = temp_dir / "shapefile"
    extraction_dir.mkdir(parents=True, exist_ok=True)

    try:
        with ZipFile(path) as archive:
            names = archive.namelist()

            # Prevent path traversal attacks.
            if any(
                Path(name).is_absolute() or ".." in Path(name).parts
                for name in names
            ):
                raise ValueError("The ZIP contains unsafe file paths.")

            archive.extractall(extraction_dir)

    except BadZipFile as exc:
        raise ValueError("The uploaded file is not a valid ZIP archive.") from exc

    shp_files = list(extraction_dir.rglob("*.shp"))

    if not shp_files:
        raise ValueError(
            "The ZIP does not contain a .shp Shapefile."
        )

    try:
        gdf = gpd.read_file(shp_files[0])
    except Exception as exc:
        raise ValueError(
            f"Unable to read Shapefile: {exc}"
        ) from exc

    validate_gdf(gdf, "Shapefile")
    return gdf


def validate_gdf(gdf, label: str):
    if gdf.empty:
        raise ValueError(
            f"The {label} contains no features."
        )

    if gdf.crs is None:
        raise ValueError(
            f"The {label} does not contain a CRS."
        )


def prepare_measurement_crs(gdf):
    """
    Transform geographic coordinates into a projected CRS
    before calculating area or length.
    """

    if gdf.crs is None:
        raise ValueError(
            "The file does not contain a coordinate reference system (CRS)."
        )

    crs = gdf.crs

    if crs.is_geographic:
        projected = gdf.estimate_utm_crs()

        if projected is None:
            projected = "EPSG:3857"

        return gdf.to_crs(projected)

    unit_name = ""

    if crs.axis_info:
        unit_name = (
            crs.axis_info[0].unit_name or ""
        ).lower()

    if unit_name not in {
        "metre",
        "meter",
        "metres",
        "meters",
    }:
        wgs84 = gdf.to_crs("EPSG:4326")

        projected = (
            wgs84.estimate_utm_crs()
            or "EPSG:3857"
        )

        return wgs84.to_crs(projected)

    return gdf


def calculate_measurements(gdf, filename: str) -> dict:
    measurement_gdf = prepare_measurement_crs(gdf)

    original_crs = gdf.crs.to_string()
    measurement_crs = measurement_gdf.crs.to_string()

    # Convert original features to GeoJSON so that geometry
    # and properties can be returned and stored in SQLite.
    original_features = json.loads(
        gdf.to_json(
            drop_id=False,
            na="null"
        )
    )["features"]

    features = []

    for index, (geometry, original_feature) in enumerate(
        zip(
            measurement_gdf.geometry,
            original_features
        )
    ):

        if geometry is None or geometry.is_empty:
            continue

        geometry_type = geometry.geom_type

        feature = {
            "id": index,
            "geometry_type": geometry_type,

            # Original geometry in GeoJSON format.
            "geometry": original_feature.get("geometry"),

            # Original feature attributes.
            "properties": original_feature.get(
                "properties",
                {}
            ),

            "crs": original_crs,

            "measurement_supported": True,
        }

        # Polygon
        if geometry_type in {
            "Polygon",
            "MultiPolygon",
        }:
            feature["area_m2"] = round(
                float(geometry.area),
                3
            )

            # Extra useful measurement.
            feature["perimeter_m"] = round(
                float(geometry.length),
                3
            )

        # Line
        elif geometry_type in {
            "LineString",
            "MultiLineString",
        }:
            feature["length_m"] = round(
                float(geometry.length),
                3
            )

        # Point
        elif geometry_type in {
            "Point",
            "MultiPoint",
        }:
            feature["measurement_supported"] = False

            feature["message"] = (
                "No measurement is required "
                "for Point geometries."
            )

        # Anything else
        else:
            feature["measurement_supported"] = False

            feature["message"] = (
                f"Measurement is not supported "
                f"for {geometry_type}."
            )

        features.append(feature)

    return {
        "file_name": filename,
        "original_crs": original_crs,
        "measurement_crs": measurement_crs,
        "feature_count": len(features),
        "features": features,
    }