from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile

import geopandas as gpd
from shapely.geometry import Polygon

from app.services.measurement import process_geospatial_file


def test_shapefile_zip_processing():
    with TemporaryDirectory() as temp:
        temp_path = Path(temp)
        shp_path = temp_path / "land.shp"
        gdf = gpd.GeoDataFrame(
            {"name": ["land"]},
            geometry=[Polygon([(0, 0), (100, 0), (100, 100), (0, 100)])],
            crs="EPSG:32645",
        )
        gdf.to_file(shp_path, driver="ESRI Shapefile")

        zip_path = temp_path / "land.zip"
        with ZipFile(zip_path, "w") as archive:
            for sidecar in temp_path.glob("land.*"):
                archive.write(sidecar, sidecar.name)

        result = process_geospatial_file("land.zip", zip_path.read_bytes())
        feature = result["features"][0]
        assert feature["geometry_type"] == "Polygon"
        assert feature["area_m2"] == 10000.0
