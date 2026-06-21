from __future__ import annotations

import json
import math
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

import numpy as np
import pandas as pd
from catboost import CatBoostRegressor

from surplussync_ml.canonical import CANONICAL_DATE, CANONICAL_SCHOOL_ID, canonical_forecast
from surplussync_ml.config import settings
from surplussync_ml.contracts import ForecastFeatures, ForecastResponse, Influence, MenuPrediction
from surplussync_ml.features import prepare_features

RiskLevel = Literal["low", "moderate", "high", "critical"]


def _risk_level(preventable: int) -> RiskLevel:
    if preventable >= 200:
        return "critical"
    if preventable >= 100:
        return "high"
    if preventable >= 20:
        return "moderate"
    return "low"


class ForecastEngine:
    def __init__(
        self,
        model_dir: Path | None = None,
        *,
        allow_demo_fixture: bool | None = None,
    ) -> None:
        self.model_dir = model_dir or settings.model_dir
        self.allow_demo_fixture = (
            settings.allow_demo_fixture if allow_demo_fixture is None else allow_demo_fixture
        )
        self.point: CatBoostRegressor | None = None
        self.low: CatBoostRegressor | None = None
        self.high: CatBoostRegressor | None = None
        self.metadata: dict[str, object] = {}
        self._load()

    @property
    def trained(self) -> bool:
        return self.point is not None and self.low is not None and self.high is not None

    def _load(self) -> None:
        required = ["attendance_point.cbm", "attendance_q10.cbm", "attendance_q90.cbm"]
        if not all((self.model_dir / name).exists() for name in required):
            return
        self.point = CatBoostRegressor()
        self.low = CatBoostRegressor()
        self.high = CatBoostRegressor()
        self.point.load_model(self.model_dir / required[0])
        self.low.load_model(self.model_dir / required[1])
        self.high.load_model(self.model_dir / required[2])
        meta = self.model_dir / "metadata.json"
        if meta.exists():
            self.metadata = json.loads(meta.read_text(encoding="utf-8"))

    def predict(self, request: ForecastFeatures) -> ForecastResponse:
        if (
            self.allow_demo_fixture
            and request.school_id == CANONICAL_SCHOOL_ID
            and request.date == CANONICAL_DATE
        ):
            return canonical_forecast()
        if not self.trained:
            raise RuntimeError("model artifacts are missing; run the training workstream first")

        point_model = self.point
        low_model = self.low
        high_model = self.high
        assert point_model is not None and low_model is not None and high_model is not None

        row = request.model_dump()
        row["weekday"] = request.date.strftime("%A")
        row["month"] = request.date.month
        row["week_of_year"] = request.date.isocalendar().week
        features = prepare_features(pd.DataFrame([row]))
        point = int(round(float(point_model.predict(features)[0])))
        low = int(math.floor(float(low_model.predict(features)[0])))
        high = int(math.ceil(float(high_model.predict(features)[0])))
        low, high = min(low, high), max(low, high)
        point = int(np.clip(point, 0, request.eligible))
        low = int(np.clip(low, 0, request.eligible))
        high = int(np.clip(high, 0, request.eligible))
        safety_floor = high + settings.safety_buffer_meals
        recommended = min(request.eligible, max(point + 20, safety_floor))
        floor_applied = recommended == min(request.eligible, safety_floor)
        preventable = max(request.normal_prep - recommended, 0)
        shortage_prob = round(max(0.005, min(0.35, (point - recommended + 35) / 220)), 3)
        large_surplus_prob = round(
            max(0.01, min(0.95, (request.normal_prep - point - 40) / 230)),
            3,
        )
        risk = _risk_level(preventable)
        influences = self._influences(request)
        menu = [MenuPrediction(item=request.menu_name, recommended=recommended)]
        return ForecastResponse(
            date=request.date,
            expectedAttendance=point,
            intervalLow=low,
            intervalHigh=high,
            recommendedPrep=recommended,
            shortageProb=shortage_prob,
            largeSurplusProb=large_surplus_prob,
            preventableSurplus=preventable,
            risk=risk,
            dataQuality="medium",
            modelVersion=str(self.metadata.get("modelVersion", "ssp-forecast-ml-0.1.0")),
            menu=menu,
            influences=influences,
            similarDays=[],
            approvalRequired=True,
            decisionStatus="PROPOSED",
            safetyFloorApplied=floor_applied,
            generatedAt=datetime.now(UTC),
        )

    @staticmethod
    def _influences(request: ForecastFeatures) -> list[Influence]:
        items: list[Influence] = []
        if request.trip_students:
            items.append(
                Influence(
                    factor="Field trip",
                    direction="down",
                    magnitude=round(request.trip_students * 0.82),
                    note=f"{request.trip_students} students expected off-campus",
                )
            )
        if request.early_dismissal:
            items.append(
                Influence(
                    factor="Early dismissal",
                    direction="down",
                    magnitude=62,
                    note="Shortened school day",
                )
            )
        if request.is_exam:
            items.append(
                Influence(
                    factor="Examination schedule",
                    direction="down",
                    magnitude=36,
                    note="Alternate attendance pattern",
                )
            )
        if request.rain_probability >= 0.6:
            items.append(
                Influence(
                    factor="Rain forecast",
                    direction="down",
                    magnitude=round(23 * min(request.rain_inches, 1.4) * request.rain_probability),
                    note=f"{request.rain_probability:.0%} rain probability",
                )
            )
        if request.menu_popularity > 1.02:
            items.append(
                Influence(
                    factor=f"Popular menu: {request.menu_name}",
                    direction="up",
                    magnitude=round(215 * (request.menu_popularity - 1)),
                    note="Historical menu participation above baseline",
                )
            )
        return items
