#!/bin/sh
set -eu

cd "$(dirname "$0")/.."

python -m surplussync_ml.bootstrap

exec uvicorn surplussync_ml.api.main:app \
  --host "${HOST:-0.0.0.0}" \
  --port "${PORT:-8000}"
