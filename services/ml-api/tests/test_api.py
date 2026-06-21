from fastapi.testclient import TestClient

from surplussync_ml.api.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_canonical_forecast_endpoint() -> None:
    response = client.post("/v1/forecast", json={"school_id": "lhphs", "date": "2026-03-12"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["expectedAttendance"] == 528
    assert payload["recommendedPrep"] == 562
    assert payload["approvalRequired"] is True
