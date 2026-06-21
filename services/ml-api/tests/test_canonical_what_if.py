from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from surplussync_ml.api.main import create_app
from surplussync_ml.canonical import canonical_forecast, canonical_trip_cancelled_what_if
from surplussync_ml.config import Settings
from surplussync_ml.modeling.service import ForecastEngine

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"
CANONICAL_WHAT_IF = json.loads((EXAMPLES / "what_if_request.json").read_text(encoding="utf-8"))
NONCANONICAL_WHAT_IF = {
    "base": {
        "school_id": "lhphs",
        "date": "2026-03-13",
        "enrolled": 820,
        "eligible": 760,
        "normal_prep": 730,
        "menu_name": "Cheese pizza",
        "menu_popularity": 1.075,
    },
    "changes": {
        "trip_students": 80,
        "rain_probability": 0.7,
        "rain_inches": 0.9,
    },
}


def test_canonical_baseline_fixture_values() -> None:
    baseline = canonical_forecast()
    assert baseline.expectedAttendance == 528
    assert baseline.intervalLow == 497
    assert baseline.intervalHigh == 557
    assert baseline.recommendedPrep == 562
    assert baseline.preventableSurplus == 168
    assert baseline.shortageProb == 0.041
    assert baseline.approvalRequired is True
    assert baseline.decisionStatus == "PROPOSED"


def test_canonical_trip_cancelled_fixture_values() -> None:
    corrected = canonical_trip_cancelled_what_if()
    assert corrected.expectedAttendance == 540
    assert corrected.intervalLow == 512
    assert corrected.intervalHigh == 568
    assert corrected.recommendedPrep == 575
    assert corrected.preventableSurplus == 155
    assert corrected.shortageProb == 0.034
    assert corrected.risk == "high"
    assert corrected.safetyFloorApplied is True
    assert corrected.recommendedPrep - corrected.intervalHigh == 7
    assert corrected.approvalRequired is True
    assert corrected.decisionStatus == "PROPOSED"


def test_canonical_trip_cancelled_what_if_endpoint() -> None:
    client = TestClient(create_app())
    response = client.post("/v1/what-if", json=CANONICAL_WHAT_IF)
    assert response.status_code == 200
    payload = response.json()
    assert payload["expectedAttendance"] == 540
    assert payload["intervalLow"] == 512
    assert payload["intervalHigh"] == 568
    assert payload["recommendedPrep"] == 575
    assert payload["preventableSurplus"] == 155
    assert payload["shortageProb"] == 0.034
    assert payload["risk"] == "high"
    assert payload["safetyFloorApplied"] is True
    assert payload["recommendedPrep"] - payload["intervalHigh"] == 7
    assert payload["approvalRequired"] is True
    assert payload["decisionStatus"] == "PROPOSED"
    assert payload["expectedAttendance"] != 528
    assert payload["recommendedPrep"] != 562


def test_unsupported_canonical_what_if_returns_422() -> None:
    client = TestClient(create_app())
    unsupported = {
        **CANONICAL_WHAT_IF,
        "changes": {"trip_students": 0},
    }
    response = client.post("/v1/what-if", json=unsupported)
    assert response.status_code == 422
    assert response.json()["detail"] == "Unsupported canonical demo what-if scenario"


def test_fixture_disabled_canonical_what_if_uses_model_path(tmp_path: Path) -> None:
    settings = Settings(
        model_dir=Path("artifacts/models"),
        allow_demo_fixture=False,
    )
    engine = ForecastEngine(
        model_dir=Path("artifacts/models"),
        allow_demo_fixture=False,
    )
    if not engine.trained:
        return
    client = TestClient(create_app(app_settings=settings, engine=engine))
    response = client.post("/v1/what-if", json=CANONICAL_WHAT_IF)
    assert response.status_code == 200
    payload = response.json()
    assert payload["expectedAttendance"] not in {528, 540}
    assert payload["modelVersion"] == "ssp-forecast-ml-0.1.0"
    assert payload["dataQuality"] == "medium"


def test_noncanonical_what_if_behavior_unchanged() -> None:
    client = TestClient(create_app())
    response = client.post("/v1/what-if", json=NONCANONICAL_WHAT_IF)
    assert response.status_code == 200
    payload = response.json()
    assert payload["date"] == "2026-03-13"
    assert payload["modelVersion"] == "ssp-forecast-ml-0.1.0"
    assert payload["dataQuality"] == "medium"
    assert payload["approvalRequired"] is True
    assert payload["decisionStatus"] == "PROPOSED"
