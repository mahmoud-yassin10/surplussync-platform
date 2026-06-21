from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

MENUS = {
    "Chicken & rice": 1.061,
    "Turkey sandwich": 0.985,
    "Veggie pasta": 0.955,
    "Beef chili": 1.015,
    "Cheese pizza": 1.075,
    "Grain bowl": 0.945,
}


def generate(seed: int = 20260312) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range("2023-08-21", "2026-06-12")
    frame = pd.DataFrame({"date": dates})
    frame = frame[~frame["date"].dt.month.isin([7])].reset_index(drop=True)
    n = len(frame)
    frame["school_id"] = "lhphs"
    frame["enrolled"] = 820
    frame["eligible"] = 760
    frame["normal_prep"] = 730
    frame["weekday"] = frame["date"].dt.day_name()
    frame["month"] = frame["date"].dt.month
    frame["week_of_year"] = frame["date"].dt.isocalendar().week.astype(int)
    frame["is_exam"] = rng.binomial(1, 0.10, n)
    frame["trip_students"] = np.where(rng.random(n) < 0.075, rng.integers(25, 125, n), 0)
    frame["early_dismissal"] = rng.binomial(1, 0.035, n)
    frame["assembly_students"] = np.where(rng.random(n) < 0.05, rng.integers(30, 180, n), 0)
    frame["sports_students"] = np.where(rng.random(n) < 0.08, rng.integers(10, 55, n), 0)
    seasonal_rain = 0.30 + 0.18 * np.sin((frame["month"] - 2) / 12 * 2 * np.pi)
    frame["rain_probability"] = np.clip(rng.beta(2, 4, n) + seasonal_rain * 0.25, 0, 1)
    frame["rain_inches"] = np.where(frame["rain_probability"] > 0.55, rng.gamma(1.4, 0.55, n), 0)
    frame["temperature_f"] = (
        54 + 22 * np.sin((frame["month"] - 4) / 12 * 2 * np.pi) + rng.normal(0, 7, n)
    )
    menu_names = np.array(list(MENUS))
    frame["menu_name"] = menu_names[np.arange(n) % len(menu_names)]
    frame["menu_popularity"] = frame["menu_name"].map(MENUS).astype(float)

    weekday_effect = (
        frame["weekday"]
        .map({"Monday": 4, "Tuesday": 0, "Wednesday": -5, "Thursday": -2, "Friday": -20})
        .astype(float)
    )
    base = 704 + weekday_effect
    attendance = (
        base
        - 36 * frame["is_exam"]
        - 0.82 * frame["trip_students"]
        - 62 * frame["early_dismissal"]
        - 0.23 * frame["assembly_students"]
        - 0.42 * frame["sports_students"]
        - 23 * (frame["rain_probability"] * np.minimum(frame["rain_inches"], 1.4))
        + 215 * (frame["menu_popularity"] - 1.0)
        + rng.normal(0, 13, n)
    )
    frame["actual_attendance"] = np.clip(np.rint(attendance), 300, 790).astype(int)
    frame["recent_attendance_7d"] = (
        frame["actual_attendance"].shift(1).rolling(5, min_periods=1).mean().fillna(704)
    )
    frame["recent_attendance_14d"] = (
        frame["actual_attendance"].shift(1).rolling(10, min_periods=1).mean().fillna(702)
    )
    frame["expected_attendance"] = np.rint(
        0.58 * frame["recent_attendance_7d"] + 0.42 * frame["recent_attendance_14d"]
    ).astype(int)
    frame["prepared_meals"] = frame["normal_prep"]
    frame["served_meals"] = np.minimum(
        frame["prepared_meals"], np.maximum(frame["actual_attendance"] - rng.integers(5, 14, n), 0)
    )
    surplus = frame["prepared_meals"] - frame["served_meals"]
    recoverable_ratio = np.where(
        frame["menu_name"].isin(["Turkey sandwich", "Cheese pizza"]), 0.82, 0.68
    )
    frame["recoverable_surplus"] = np.rint(surplus * recoverable_ratio).astype(int)
    frame["nonrecoverable_surplus"] = surplus - frame["recoverable_surplus"]

    canonical = {
        "date": pd.Timestamp("2026-03-12"),
        "school_id": "lhphs",
        "enrolled": 820,
        "eligible": 760,
        "normal_prep": 730,
        "weekday": "Thursday",
        "month": 3,
        "week_of_year": 11,
        "is_exam": 1,
        "trip_students": 112,
        "early_dismissal": 1,
        "assembly_students": 0,
        "sports_students": 0,
        "rain_probability": 0.78,
        "rain_inches": 1.08,
        "temperature_f": 46.0,
        "menu_name": "Chicken & rice",
        "menu_popularity": 1.061,
        "recent_attendance_7d": 708.0,
        "recent_attendance_14d": 706.0,
        "expected_attendance": 528,
        "actual_attendance": 528,
        "prepared_meals": 730,
        "served_meals": 562,
        "recoverable_surplus": 118,
        "nonrecoverable_surplus": 50,
    }
    mask = frame["date"] == canonical["date"]
    if mask.any():
        for key, value in canonical.items():
            frame.loc[mask, key] = value
    else:
        frame = pd.concat([frame, pd.DataFrame([canonical])], ignore_index=True)
    return frame.sort_values("date").reset_index(drop=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", type=Path, default=Path("data/generated/synthetic_school_days.csv")
    )
    parser.add_argument("--seed", type=int, default=20260312)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    data = generate(args.seed)
    data.to_csv(args.output, index=False)
    print(f"wrote {len(data)} rows to {args.output}")


if __name__ == "__main__":
    main()
