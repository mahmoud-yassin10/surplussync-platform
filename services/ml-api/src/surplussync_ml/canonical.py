from __future__ import annotations

from datetime import UTC, date, datetime

from .contracts import ForecastFeatures, ForecastResponse, WhatIfRequest

CANONICAL_SCHOOL_ID = "lhphs"
CANONICAL_DATE = date(2026, 3, 12)

CANONICAL_BASE_PAYLOAD: dict[str, object] = {
    "school_id": CANONICAL_SCHOOL_ID,
    "date": CANONICAL_DATE.isoformat(),
    "enrolled": 820,
    "eligible": 760,
    "normal_prep": 730,
    "expected_attendance": 528,
    "is_exam": True,
    "trip_students": 112,
    "early_dismissal": True,
    "rain_probability": 0.78,
    "rain_inches": 1.08,
    "temperature_f": 46,
    "menu_name": "Chicken & rice",
    "menu_popularity": 1.061,
    "recent_attendance_7d": 708,
    "recent_attendance_14d": 706,
}

CANONICAL_TRIP_CANCELLED_CHANGES: dict[str, int] = {
    "trip_students": 0,
    "expected_attendance": 540,
}


def canonical_base_features() -> ForecastFeatures:
    return ForecastFeatures.model_validate(CANONICAL_BASE_PAYLOAD)


def is_canonical_base(base: ForecastFeatures) -> bool:
    return base == canonical_base_features()


def is_canonical_demo_scope(request: WhatIfRequest) -> bool:
    return (
        request.base.school_id == CANONICAL_SCHOOL_ID
        and request.base.date == CANONICAL_DATE
        and is_canonical_base(request.base)
    )


def is_canonical_trip_cancelled_what_if(request: WhatIfRequest) -> bool:
    if not is_canonical_demo_scope(request):
        return False
    if set(request.changes) != set(CANONICAL_TRIP_CANCELLED_CHANGES):
        return False
    return all(
        request.changes[key] == value for key, value in CANONICAL_TRIP_CANCELLED_CHANGES.items()
    )


def canonical_forecast() -> ForecastResponse:
    return ForecastResponse.model_validate(
        {
            "date": "2026-03-12",
            "expectedAttendance": 528,
            "intervalLow": 497,
            "intervalHigh": 557,
            "recommendedPrep": 562,
            "shortageProb": 0.041,
            "largeSurplusProb": 0.12,
            "preventableSurplus": 168,
            "risk": "high",
            "dataQuality": "high",
            "modelVersion": "ssp-forecast-1.0",
            "menu": [
                {"item": "Chicken portions", "recommended": 548},
                {"item": "Rice portions", "recommended": 562},
                {"item": "Vegetable sides", "recommended": 520},
                {"item": "Fruit cups", "recommended": 535},
                {"item": "Packaged milk", "recommended": 555},
            ],
            "influences": _baseline_influences(),
            "similarDays": _similar_days(),
            "approvalRequired": True,
            "decisionStatus": "PROPOSED",
            "safetyFloorApplied": True,
            "generatedAt": datetime.now(UTC),
        }
    )


def canonical_trip_cancelled_what_if() -> ForecastResponse:
    return ForecastResponse.model_validate(
        {
            "date": "2026-03-12",
            "expectedAttendance": 540,
            "intervalLow": 512,
            "intervalHigh": 568,
            "recommendedPrep": 575,
            "shortageProb": 0.034,
            "largeSurplusProb": 0.12,
            "preventableSurplus": 155,
            "risk": "high",
            "dataQuality": "high",
            "modelVersion": "ssp-forecast-1.0",
            "menu": [
                {"item": "Chicken portions", "recommended": 561},
                {"item": "Rice portions", "recommended": 575},
                {"item": "Vegetable sides", "recommended": 533},
                {"item": "Fruit cups", "recommended": 548},
                {"item": "Packaged milk", "recommended": 568},
            ],
            "influences": _trip_cancelled_influences(),
            "similarDays": _similar_days(),
            "approvalRequired": True,
            "decisionStatus": "PROPOSED",
            "safetyFloorApplied": True,
            "generatedAt": datetime.now(UTC),
        }
    )


def _baseline_influences() -> list[dict[str, object]]:
    return [
        {
            "factor": "Grade 10 field trip",
            "direction": "down",
            "magnitude": 92,
            "note": "112 students off-campus, 09:30–14:00",
        },
        {
            "factor": "Early dismissal",
            "direction": "down",
            "magnitude": 64,
            "note": "All grades released 12:45",
        },
        {
            "factor": "Midterm examinations",
            "direction": "down",
            "magnitude": 38,
            "note": "Grades 11–12 alternate schedule",
        },
        {
            "factor": "Heavy rain forecast",
            "direction": "down",
            "magnitude": 22,
            "note": "NWS 78% probability >1in rainfall",
        },
        {
            "factor": "Popular menu: chicken & rice",
            "direction": "up",
            "magnitude": 14,
            "note": "Historical participation +6.1% vs baseline",
        },
        {
            "factor": "Recent attendance trend",
            "direction": "up",
            "magnitude": 6,
            "note": "Trailing 14-day average rising",
        },
    ]


def _trip_cancelled_influences() -> list[dict[str, object]]:
    influences = _baseline_influences()
    influences[0] = {
        "factor": "Grade 10 field trip",
        "direction": "down",
        "magnitude": 0,
        "note": "Trip cancelled — input removed",
    }
    return influences


def _similar_days() -> list[dict[str, object]]:
    return [
        {
            "date": "2025-10-23",
            "attendance": 541,
            "note": "Midterms + Gr. 9 trip",
        },
        {
            "date": "2025-12-04",
            "attendance": 519,
            "note": "Early dismissal + storm",
        },
        {
            "date": "2026-01-29",
            "attendance": 552,
            "note": "Exams + assembly",
        },
    ]
