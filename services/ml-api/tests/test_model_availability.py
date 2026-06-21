from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from surplussync_ml.api.main import create_app
from surplussync_ml.config import Settings
from surplussync_ml.modeling.service import ForecastEngine

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"
CANONICAL_REQUEST = json.loads((EXAMPLES / "canonical_request.json").read_text(encoding="utf-8"))
NONCANONICAL_REQUEST = json.loads(
    (EXAMPLES / "noncanonical_request.json").read_text(encoding="utf-8")
)


def _client(tmp_path: Path, *, allow_demo_fixture: bool) -> TestClient:
    settings = Settings(
        model_dir=tmp_path,
        allow_demo_fixture=allow_demo_fixture,
    )
    engine = ForecastEngine(model_dir=tmp_path, allow_demo_fixture=allow_demo_fixture)
    return TestClient(create_app(app_settings=settings, engine=engine))


def test_missing_models_canonical_works_with_demo_fixture(tmp_path: Path) -> None:
    client = _client(tmp_path, allow_demo_fixture=True)
    response = client.post("/v1/forecast", json=CANONICAL_REQUEST)
    assert response.status_code == 200
    assert response.json()["expectedAttendance"] == 528


def test_missing_models_noncanonical_returns_503(tmp_path: Path) -> None:
    client = _client(tmp_path, allow_demo_fixture=True)
    response = client.post("/v1/forecast", json=NONCANONICAL_REQUEST)
    assert response.status_code == 503
    assert "model artifacts are missing" in response.json()["detail"]


def test_production_config_disables_canonical_fixture(tmp_path: Path) -> None:
    client = _client(tmp_path, allow_demo_fixture=False)
    response = client.post("/v1/forecast", json=CANONICAL_REQUEST)
    assert response.status_code == 503
    assert "model artifacts are missing" in response.json()["detail"]
