from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from surplussync_ml.api.main import create_app

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"
LOCKED_FIELDS = (
    "date",
    "expectedAttendance",
    "intervalLow",
    "intervalHigh",
    "recommendedPrep",
    "preventableSurplus",
    "approvalRequired",
    "decisionStatus",
)


def test_canonical_forecast_matches_contract_fixture() -> None:
    fixture = json.loads((EXAMPLES / "canonical_response.json").read_text(encoding="utf-8"))
    request = json.loads((EXAMPLES / "canonical_request.json").read_text(encoding="utf-8"))
    client = TestClient(create_app())
    response = client.post("/v1/forecast", json=request)
    assert response.status_code == 200
    payload = response.json()
    for field in LOCKED_FIELDS:
        assert payload[field] == fixture[field], field
    assert payload["menu"] == fixture["menu"]
    assert payload["influences"] == fixture["influences"]
    assert payload["similarDays"] == fixture["similarDays"]
    assert "generatedAt" in payload
