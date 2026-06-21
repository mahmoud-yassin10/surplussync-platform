# Quickstart

## Prerequisites

- Bun 1.3.14 or compatible
- Node.js 22
- Python 3.13
- PowerShell on Windows

## Ports

- ML: `8000`
- AI assistant: `3001`
- Frontend: usually `3000`; Vite prints the active port

## Environment

Copy the root environment example:

```powershell
Copy-Item .env.example .env
```

`GEMINI_API_KEY` is optional. Without it, the AI assistant uses deterministic language fallback.

## Windows Startup

```powershell
cd services/ml-api
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
deactivate
cd ..\..

cd services/copilot-api
npm ci
cd ..\..

cd apps/web
bun install --frozen-lockfile
cd ..\..

.\scripts\start.ps1
.\scripts\verify.ps1
```

## Linux/macOS Startup

```bash
cp .env.example .env
cd services/ml-api
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
uvicorn surplussync_ml.api.main:app --host 127.0.0.1 --port 8000
```

In separate terminals:

```bash
cd services/copilot-api
PORT=3001 ML_SERVICE_URL=http://127.0.0.1:8000 npm run dev
```

```bash
cd apps/web
ML_SERVICE_URL=http://127.0.0.1:8000 COPILOT_SERVICE_URL=http://127.0.0.1:3001 bun run dev
```

## Shutdown

On Windows, use:

```powershell
.\scripts\stop.ps1
```

This only stops PIDs recorded by `start.ps1`.

## Common Problems

- Port already in use: stop the conflicting service or let Vite choose another frontend port.
- Python cannot run scripts: check execution policy and activate `.venv`.
- ML model not loaded: confirm `services/ml-api/artifacts/models` contains committed `.cbm` files.
- Missing Gemini key: expected; deterministic fallback is used.
- Frozen lockfile failure: rerun installs in the service directory and do not mix package managers.
