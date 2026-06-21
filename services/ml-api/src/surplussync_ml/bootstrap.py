from __future__ import annotations

import json
import sys
from pathlib import Path

from surplussync_ml.config import settings
from surplussync_ml.data.synthetic import generate
from surplussync_ml.modeling.train import train

REQUIRED_MODELS = (
    "attendance_point.cbm",
    "attendance_q10.cbm",
    "attendance_q90.cbm",
)


def models_present(model_dir: Path) -> bool:
    return all((model_dir / name).exists() for name in REQUIRED_MODELS)


def ensure_models() -> Path:
    model_dir = settings.model_dir
    if models_present(model_dir):
        return model_dir

    data_path = settings.data_path
    data_path.parent.mkdir(parents=True, exist_ok=True)
    if not data_path.exists():
        generate().to_csv(data_path, index=False)

    metadata = train(data_path, model_dir)
    print(json.dumps({"status": "trained", "modelDir": str(model_dir), **metadata}, indent=2))
    return model_dir


def main() -> None:
    try:
        ensure_models()
    except Exception as exc:  # noqa: BLE001 - bootstrap must surface any training failure
        print(f"model bootstrap failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
