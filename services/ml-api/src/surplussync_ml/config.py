from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _parse_bool(value: str | None, *, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _parse_origins(value: str | None) -> tuple[str, ...]:
    if not value or not value.strip():
        return ()
    return tuple(origin.strip() for origin in value.split(",") if origin.strip())


def _env(primary: str, legacy: str, default: str) -> str:
    return os.getenv(primary, os.getenv(legacy, default))


@dataclass(frozen=True)
class Settings:
    host: str = "0.0.0.0"
    port: int = 8000
    allowed_origins: tuple[str, ...] = ()
    model_dir: Path = Path("artifacts/models")
    data_path: Path = Path("data/generated/synthetic_school_days.csv")
    allow_demo_fixture: bool = True
    safety_buffer_meals: int = 5

    @classmethod
    def from_env(cls) -> Settings:
        return cls(
            host=_env("HOST", "SURPLUSSYNC_HOST", "0.0.0.0"),
            port=int(_env("PORT", "SURPLUSSYNC_PORT", "8000")),
            allowed_origins=_parse_origins(
                _env("ALLOWED_ORIGINS", "SURPLUSSYNC_ALLOWED_ORIGINS", "")
            ),
            model_dir=Path(_env("MODEL_DIR", "SURPLUSSYNC_MODEL_DIR", "artifacts/models")),
            data_path=Path(
                os.getenv("SURPLUSSYNC_DATA_PATH", "data/generated/synthetic_school_days.csv")
            ),
            allow_demo_fixture=_parse_bool(
                _env("ALLOW_DEMO_FIXTURE", "SURPLUSSYNC_ALLOW_DEMO_FIXTURE", "true"),
                default=True,
            ),
        )


settings = Settings.from_env()
