from __future__ import annotations

import argparse
import json
import platform
from pathlib import Path

import catboost
import numpy as np
import pandas as pd
import sklearn
from catboost import CatBoostRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from surplussync_ml.features import CATEGORICAL_FEATURES, FEATURE_NAMES, TARGET, prepare_features


def _model(loss_function: str, seed: int) -> CatBoostRegressor:
    return CatBoostRegressor(
        iterations=80,
        depth=5,
        learning_rate=0.045,
        loss_function=loss_function,
        random_seed=seed,
        verbose=False,
        allow_writing_files=False,
    )


def train(data_path: Path, output_dir: Path, seed: int = 20260312) -> dict[str, object]:
    frame = pd.read_csv(data_path).sort_values("date").reset_index(drop=True)
    split = int(len(frame) * 0.8)
    train_df, test_df = frame.iloc[:split], frame.iloc[split:]
    x_train, x_test = prepare_features(train_df), prepare_features(test_df)
    y_train, y_test = train_df[TARGET], test_df[TARGET]

    point = _model("RMSE", seed)
    low = _model("Quantile:alpha=0.10", seed + 1)
    high = _model("Quantile:alpha=0.90", seed + 2)
    for model in (point, low, high):
        model.fit(x_train, y_train, cat_features=CATEGORICAL_FEATURES)

    pred = point.predict(x_test)
    q10 = low.predict(x_test)
    q90 = high.predict(x_test)
    lower = np.minimum(q10, q90)
    upper = np.maximum(q10, q90)
    weekday_baseline = train_df.groupby("weekday")[TARGET].mean()
    baseline_pred = test_df["weekday"].map(weekday_baseline).fillna(y_train.mean())

    metrics = {
        "mae": float(mean_absolute_error(y_test, pred)),
        "rmse": float(mean_squared_error(y_test, pred) ** 0.5),
        "r2": float(r2_score(y_test, pred)),
        "interval_80_coverage": float(np.mean((y_test >= lower) & (y_test <= upper))),
        "mean_interval_width": float(np.mean(upper - lower)),
        "weekday_baseline_mae": float(mean_absolute_error(y_test, baseline_pred)),
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    point.save_model(output_dir / "attendance_point.cbm")
    low.save_model(output_dir / "attendance_q10.cbm")
    high.save_model(output_dir / "attendance_q90.cbm")
    metadata = {
        "modelVersion": "ssp-forecast-ml-0.1.0",
        "metrics": metrics,
        "featureNames": FEATURE_NAMES,
        "categoricalFeatures": CATEGORICAL_FEATURES,
        "trainingRows": len(train_df),
        "testRows": len(test_df),
        "dataWindow": {"start": str(frame["date"].min()), "end": str(frame["date"].max())},
        "pythonVersion": platform.python_version(),
        "catboostVersion": catboost.__version__,
        "scikitLearnVersion": sklearn.__version__,
        "syntheticData": True,
    }
    (output_dir / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return metadata


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data", type=Path, default=Path("data/generated/synthetic_school_days.csv")
    )
    parser.add_argument("--output", type=Path, default=Path("artifacts/models"))
    args = parser.parse_args()
    metadata = train(args.data, args.output)
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
