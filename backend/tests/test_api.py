from fastapi.testclient import TestClient

from app.config import Settings
from app.interfaces.api import routes
from app.main import create_app


def test_health() -> None:
    client = TestClient(create_app())
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_readiness_without_database_configuration(monkeypatch) -> None:
    monkeypatch.setattr(routes, "get_settings", lambda: Settings(database_url=None))
    client = TestClient(create_app())
    response = client.get("/api/v1/readiness")
    assert response.status_code == 503
    assert response.json()["status"] == "not_ready"
