$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot

Push-Location (Join-Path $Root "apps/web")
bun install --frozen-lockfile
bunx tsc --noEmit
bun run test:run
bun run build
Pop-Location

Push-Location (Join-Path $Root "services/copilot-api")
npm ci
npm run lint
npm test
npm run build
Pop-Location

Push-Location (Join-Path $Root "services/ml-api")
if (-not (Test-Path ".venv")) {
  py -3.13 -m venv .venv
}
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m mypy src
.\.venv\Scripts\python.exe -m surplussync_ml.bootstrap
Pop-Location

Write-Host "All SurplusSync platform validations completed."
