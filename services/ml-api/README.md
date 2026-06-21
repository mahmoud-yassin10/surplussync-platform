# SurplusSync ML Service

Python 3.13 forecasting and decision-support backend for **SurplusSync Plus**.
It is intentionally separate from the two existing UI repositories.

## Locked product constraints

- Canonical demonstration school: **Lincoln Heights Public High School, Chicago, IL**.
- Canonical focus date: **2026-03-12**.
- The demo response is contract-locked to the existing frontend values.
- Forecasts are recommendations, never autonomous operational actions.
- Attendance corrections, preparation changes, partner alerts, reservations, routing,
  checklist completion, and pickup transitions require human approval in the product UI.
- The service never sends messages, reserves capacity, assigns drivers, or mutates pickup state.

## Workstreams

1. **Synthetic data** — reproducible school-day generator with calendar, weather, menu,
   attendance, preparation, service, and surplus fields.
2. **Baseline model** — CatBoost point and quantile regressors, time-ordered evaluation,
   artifact metadata, and a FastAPI inference layer.

## Setup

```bash
py -3.13 -m venv .venv       # Windows
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

macOS/Linux:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Run the parallel workstreams

Terminal A:

```bash
python -m surplussync_ml.data.synthetic   --output data/generated/synthetic_school_days.csv
```

Terminal B, after the dataset exists:

```bash
python -m surplussync_ml.modeling.train   --data data/generated/synthetic_school_days.csv   --output artifacts/models
```

Or run sequentially with `make train`.

## Start the API

```bash
uvicorn surplussync_ml.api.main:app --reload --port 8000
```

Key endpoints:

- `GET /health`
- `GET /v1/model/metadata`
- `POST /v1/forecast`
- `POST /v1/what-if`

Example forecast:

```bash
curl -X POST http://localhost:8000/v1/forecast   -H "Content-Type: application/json"   -d @examples/canonical_request.json
```

Canonical baseline contract (2026-03-12): expected attendance **528**, interval **497–557**,
recommended preparation **562**, preventable surplus **168**, shortage probability **0.041**.

Canonical trip-cancelled what-if (`examples/what_if_request.json`): expected attendance **540**,
interval **512–568**, recommended preparation **575**, preventable surplus **155**, shortage
probability **0.034**. Only this exact canonical scenario is supported when
`ALLOW_DEMO_FIXTURE=true`; other canonical what-if requests return HTTP 422.

## Repository workflow

```bash
git checkout -b feat/synthetic-data
git checkout -b feat/baseline-model
```

Suggested integration order:

1. Merge the scaffold.
2. Merge synthetic data and its schema tests.
3. Merge baseline training and evaluation.
4. Merge FastAPI inference.
5. Integrate only the forecast read path into `surplus-sync-plus`.
6. Integrate the Copilot later through its secure server-side gateway; do not expose API keys.

See `docs/ARCHITECTURE.md`, `docs/DATA_SCHEMA.md`, `docs/MODEL_CARD.md`, and
`docs/SAFETY.md`.
