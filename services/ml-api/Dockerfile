FROM python:3.13-slim-bookworm

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOST=0.0.0.0 \
    PORT=8000 \
    MODEL_DIR=artifacts/models \
    ALLOW_DEMO_FIXTURE=false \
    ALLOWED_ORIGINS=

COPY pyproject.toml README.md ./
COPY src ./src
COPY artifacts/models ./artifacts/models
COPY examples ./examples
COPY deployment ./deployment

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir .

RUN chmod +x deployment/start.sh

EXPOSE 8000

CMD ["deployment/start.sh"]
