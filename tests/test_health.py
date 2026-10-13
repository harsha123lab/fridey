from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_returns_service_status() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["assistant"] == "FRIDEY"


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_command_rejects_empty_text() -> None:
    response = client.post("/command", json={"text": ""})
    assert response.status_code == 422
