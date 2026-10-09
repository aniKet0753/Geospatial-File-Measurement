from shapely.geometry import LineString, Point, Polygon
import geopandas as gpd

from app.services.measurement import calculate_measurements


def test_polygon_area_and_perimeter():
    gdf = gpd.GeoDataFrame(
        {"name": ["square"]},
        geometry=[Polygon([(0, 0), (100, 0), (100, 100), (0, 100)])],
        crs="EPSG:32645",
    )
    result = calculate_measurements(gdf, "square.shp")
    feature = result["features"][0]
    assert feature["geometry_type"] == "Polygon"
    assert feature["area_m2"] == 10000.0
    assert feature["perimeter_m"] == 400.0


def test_line_length():
    gdf = gpd.GeoDataFrame(
        {"name": ["line"]},
        geometry=[LineString([(0, 0), (3, 4)])],
        crs="EPSG:32645",
    )
    result = calculate_measurements(gdf, "line.shp")
    assert result["features"][0]["length_m"] == 5.0


def test_point_is_supported_without_measurement():
    gdf = gpd.GeoDataFrame(
        {"name": ["point"]},
        geometry=[Point(88.36, 22.57)],
        crs="EPSG:4326",
    )
    result = calculate_measurements(gdf, "point.kml")
    feature = result["features"][0]
    assert feature["geometry_type"] == "Point"
    assert feature["measurement_supported"] is False
