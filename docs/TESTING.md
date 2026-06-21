# Testing

## Quick Smoke

```powershell
.\scripts\verify.ps1
```

The smoke check verifies ML health, canonical forecast values, canonical what-if values, Copilot health, and frontend forecast health when services are running.

## Full Frontend

```powershell
cd apps/web
bun install --frozen-lockfile
bunx tsc --noEmit
bun run test:run
bun run build
```

Expected: at least 90 tests and a production build.

## Full Copilot

```powershell
cd services/copilot-api
npm ci
npm run lint
npm test
npm run build
```

Expected: at least 110 tests and a production build.

## Full ML

```powershell
cd services/ml-api
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
pytest
ruff check .
mypy
python -m surplussync_ml.bootstrap
```

Expected: 15 pytest tests, ruff pass, mypy pass, and canonical fixture smoke.

## E2E Checklist

- ML `/health` reports model loaded.
- Baseline forecast returns 528, 497-557, 562, 168, 0.041.
- What-if returns 540, 512-568, 575, 155, 0.034.
- Frontend forecast gateway uses live ML when ML is running.
- Copilot health is ready.
- No autonomous proposal or action appears from explanation-only prompts.
- Manual mode blocks proposal execution.
- Stale sessions recover safely.
- Outage fallback is disclosed.

## Secret Scan

Search for real values matching service tokens, Gemini keys, OpenAI keys, GitHub tokens, and private keys. `.env.example` placeholders are allowed; `.env` files are not.
