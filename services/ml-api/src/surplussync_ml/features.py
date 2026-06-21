from __future__ import annotations

import pandas as pd

FEATURE_NAMES = [
    "weekday",
    "month",
    "week_of_year",
    "enrolled",
    "eligible",
    "normal_prep",
    "expected_attendance",
    "is_exam",
    "trip_students",
    "early_dismissal",
    "assembly_students",
    "sports_students",
    "rain_probability",
    "rain_inches",
    "temperature_f",
    "menu_name",
    "menu_popularity",
    "recent_attendance_7d",
    "recent_attendance_14d",
]
CATEGORICAL_FEATURES = ["weekday", "menu_name"]
TARGET = "actual_attendance"


def prepare_features(frame: pd.DataFrame) -> pd.DataFrame:
    result = frame.copy()
    result["date"] = pd.to_datetime(result["date"])
    if "weekday" not in result:
        result["weekday"] = result["date"].dt.day_name()
    if "month" not in result:
        result["month"] = result["date"].dt.month
    if "week_of_year" not in result:
        result["week_of_year"] = result["date"].dt.isocalendar().week.astype(int)
    for name in ["is_exam", "early_dismissal"]:
        result[name] = result[name].astype(int)
    return result[FEATURE_NAMES]
