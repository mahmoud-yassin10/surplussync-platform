.PHONY: install data train api test lint check clean

install:
	python -m pip install -e ".[dev]"

data:
	python -m surplussync_ml.data.synthetic --output data/generated/synthetic_school_days.csv

train: data
	python -m surplussync_ml.modeling.train --data data/generated/synthetic_school_days.csv --output artifacts/models

api:
	uvicorn surplussync_ml.api.main:app --reload --port 8000

start:
	sh deployment/start.sh

bootstrap:
	python -m surplussync_ml.bootstrap

test:
	pytest

lint:
	ruff check .

check: lint test

clean:
	rm -f data/generated/*.csv artifacts/models/*.cbm artifacts/models/*.json
