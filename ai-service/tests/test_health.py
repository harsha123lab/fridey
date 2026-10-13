from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_is_running():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["assistant"] == "FRIDEY"


def test_health_includes_model():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["model"]


def test_empty_command_is_rejected():
    response = client.post("/command", json={"text": ""})
    assert response.status_code == 422


def test_legacy_command_field_is_supported():
    response = client.post("/command", json={"command": "hello"})
    assert response.status_code in (200, 503)
