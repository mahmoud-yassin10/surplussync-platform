param(
  [switch]$SkipInstall
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$PidFile = Join-Path $PSScriptRoot ".surplussync-pids.json"

function Start-SurplusProcess {
  param(
    [string]$Name,
    [string]$WorkingDirectory,
    [string]$Command,
    [hashtable]$Environment
  )

  $envBlock = ""
  foreach ($key in $Environment.Keys) {
    $value = $Environment[$key] -replace "'", "''"
    $envBlock += "`$env:$key='$value'; "
  }
  $fullCommand = "$envBlock$Command"
  $process = Start-Process -FilePath "powershell.exe" -ArgumentList @("-NoExit", "-Command", $fullCommand) -WorkingDirectory $WorkingDirectory -PassThru
  [pscustomobject]@{ name = $Name; pid = $process.Id; path = $WorkingDirectory }
}

$mlDir = Join-Path $Root "services/ml-api"
$copilotDir = Join-Path $Root "services/copilot-api"
$webDir = Join-Path $Root "apps/web"

if (-not $SkipInstall) {
  if (-not (Test-Path (Join-Path $mlDir ".venv"))) {
    Push-Location $mlDir
    py -3.13 -m venv .venv
    .\.venv\Scripts\python.exe -m pip install --upgrade pip
    .\.venv\Scripts\python.exe -m pip install -e ".[dev]"
    Pop-Location
  }
  if (-not (Test-Path (Join-Path $copilotDir "node_modules"))) {
    Push-Location $copilotDir
    npm ci
    Pop-Location
  }
  if (-not (Test-Path (Join-Path $webDir "node_modules"))) {
    Push-Location $webDir
    bun install --frozen-lockfile
    Pop-Location
  }
}

$token = "dev-local-main-app-token-change-me"
$copilotToken = "dev-local-copilot-token-change-me"

$processes = @()
$processes += Start-SurplusProcess -Name "ml" -WorkingDirectory $mlDir -Command ".\.venv\Scripts\python.exe -m uvicorn surplussync_ml.api.main:app --host 127.0.0.1 --port 8000" -Environment @{
  ALLOW_DEMO_FIXTURE = "true"
}
$processes += Start-SurplusProcess -Name "copilot" -WorkingDirectory $copilotDir -Command "npm run dev" -Environment @{
  PORT = "3001"
  ML_SERVICE_URL = "http://127.0.0.1:8000"
  MAIN_APP_SERVICE_TOKEN = $token
  COPILOT_ALLOW_FORECAST_FALLBACK = "true"
}
$processes += Start-SurplusProcess -Name "web" -WorkingDirectory $webDir -Command "bun run dev" -Environment @{
  ML_SERVICE_URL = "http://127.0.0.1:8000"
  COPILOT_SERVICE_URL = "http://127.0.0.1:3001"
  COPILOT_SERVICE_TOKEN = $copilotToken
  MAIN_APP_SERVICE_TOKEN = $token
  ALLOW_FORECAST_FALLBACK = "true"
}

$processes | ConvertTo-Json | Set-Content -Path $PidFile -Encoding UTF8

Write-Host "SurplusSync Plus services starting..."
Write-Host "ML API:        http://127.0.0.1:8000"
Write-Host "AI assistant:  http://127.0.0.1:3001"
Write-Host "Frontend:      use the Vite URL printed in the frontend terminal, usually http://localhost:3000"
if (-not $env:GEMINI_API_KEY) {
  Write-Host "GEMINI_API_KEY is not set; deterministic language fallback will be used."
}
Write-Host "PID file: $PidFile"
