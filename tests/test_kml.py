from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
KML = Path(__file__).resolve().parents[1] / "sample_data" / "sample.kml"


def test_upload_kml_and_retrieve_results():
    with KML.open("rb") as file:
        response = client.post("/api/files/", files={"file": ("sample.kml", file, "application/vnd.google-earth.kml+xml")})

    assert response.status_code == 201, response.text
    payload = response.json()
    assert payload["status"] == "COMPLETED"
    assert payload["feature_count"] == 3

    file_id = payload["id"]
    info = client.get(f"/api/files/{file_id}/")
    assert info.status_code == 200
    assert info.json()["filename"] == "sample.kml"

    measurements = client.get(f"/api/files/{file_id}/measurements/")
    assert measurements.status_code == 200
    features = measurements.json()["features"]
    assert {feature["geometry_type"] for feature in features} == {"Polygon", "LineString", "Point"}
