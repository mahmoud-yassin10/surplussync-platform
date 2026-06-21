from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from surplussync_ml.canonical import (
    canonical_trip_cancelled_what_if,
    is_canonical_demo_scope,
    is_canonical_trip_cancelled_what_if,
)
from surplussync_ml.config import Settings, settings
from surplussync_ml.contracts import (
    ForecastFeatures,
    ForecastResponse,
    ModelMetadata,
    WhatIfRequest,
)
from surplussync_ml.features import CATEGORICAL_FEATURES, FEATURE_NAMES
from surplussync_ml.modeling.service import ForecastEngine


def _as_float_dict(value: object) -> dict[str, float]:
    if not isinstance(value, dict):
        return {}
    return {str(key): float(item) for key, item in value.items()}


def _as_str_dict(value: object) -> dict[str, str]:
    if not isinstance(value, dict):
        return {}
    return {str(key): str(item) for key, item in value.items()}


def _as_str_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value]


def _as_int(value: object, default: int = 0) -> int:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    return default


def create_app(
    app_settings: Settings | None = None,
    engine: ForecastEngine | None = None,
) -> FastAPI:
    cfg = app_settings or settings
    eng = engine or ForecastEngine(
        model_dir=cfg.model_dir,
        allow_demo_fixture=cfg.allow_demo_fixture,
    )
    application = FastAPI(title="SurplusSync ML Service", version="0.1.0")

    if cfg.allowed_origins:
        application.add_middleware(
            CORSMiddleware,
            allow_origins=list(cfg.allowed_origins),
            allow_credentials=True,
            allow_methods=["GET", "POST", "OPTIONS"],
            allow_headers=["*"],
        )

    @application.get("/health")
    def health() -> dict[str, object]:
        return {
            "status": "ok",
            "modelLoaded": eng.trained,
            "service": "surplussync-ml-service",
        }

    @application.get("/v1/model/metadata", response_model=ModelMetadata)
    def model_metadata() -> ModelMetadata:
        meta = eng.metadata
        return ModelMetadata(
            modelVersion=str(meta.get("modelVersion", "ssp-forecast-ml-0.1.0")),
            trained=eng.trained,
            metrics=_as_float_dict(meta.get("metrics", {})),
            featureNames=_as_str_list(meta.get("featureNames", FEATURE_NAMES)),
            categoricalFeatures=_as_str_list(meta.get("categoricalFeatures", CATEGORICAL_FEATURES)),
            trainingRows=_as_int(meta.get("trainingRows", 0)),
            dataWindow=_as_str_dict(meta.get("dataWindow", {})),
        )

    @application.post("/v1/forecast", response_model=ForecastResponse)
    def forecast(request: ForecastFeatures) -> ForecastResponse:
        try:
            return eng.predict(request)
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

    @application.post("/v1/what-if", response_model=ForecastResponse)
    def what_if(request: WhatIfRequest) -> ForecastResponse:
        allowed = set(ForecastFeatures.model_fields)
        invalid = set(request.changes) - allowed
        if invalid:
            raise HTTPException(
                status_code=422,
                detail=f"Unsupported what-if fields: {sorted(invalid)}",
            )
        if cfg.allow_demo_fixture and is_canonical_demo_scope(request):
            if is_canonical_trip_cancelled_what_if(request):
                return canonical_trip_cancelled_what_if()
            raise HTTPException(
                status_code=422,
                detail="Unsupported canonical demo what-if scenario",
            )

        simulated = request.base.model_copy(update=request.changes)
        return forecast(simulated)

    return application


app = create_app()


def run() -> None:
    import uvicorn

    uvicorn.run(
        "surplussync_ml.api.main:app",
        host=settings.host,
        port=settings.port,
        reload=False,
    )
