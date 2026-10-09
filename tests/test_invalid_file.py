from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_rejects_unsupported_extension():
    response = client.post(
        "/api/files/",
        files={"file": ("notes.txt", b"hello", "text/plain")},
    )
    assert response.status_code == 415


def test_rejects_invalid_zip():
    response = client.post(
        "/api/files/",
        files={"file": ("broken.zip", b"not a zip", "application/zip")},
    )
    assert response.status_code == 400
