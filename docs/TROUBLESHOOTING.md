# Troubleshooting

## Port Already in Use

ML expects `8000`, assistant expects `3001`, and the frontend normally starts on `3000`. Stop only known SurplusSync processes or use the printed Vite URL.

## ML Model Not Loaded

Confirm committed model artifacts exist in `services/ml-api/artifacts/models`. Reinstall ML dependencies and run `python -m surplussync_ml.bootstrap`.

## Copilot Unavailable

Check `services/copilot-api`, run `npm ci`, and start with `PORT=3001`. The frontend has deterministic fallback behavior for local demo continuity.

## Missing Gemini Key

Expected for local demos. `GEMINI_API_KEY` is optional.

## Stale Session

Use the UI reset or call the assistant reset endpoint through the frontend gateway.

## Wrong Vite Port

Use the URL printed by `bun run dev` or `scripts/start.ps1`.

## Windows Execution Policy

If script execution is blocked, run PowerShell as the current user and allow local scripts according to your machine policy.

## Bun Missing

Install Bun and rerun `bun install --frozen-lockfile` in `apps/web`.

## Python Virtual Environment

Create `.venv` under `services/ml-api` with Python 3.13 and install `.[dev]`.

## Frozen Lockfile Failure

Do not mix npm/yarn/pnpm with the frontend. Use Bun for `apps/web` and npm for `services/copilot-api`.
