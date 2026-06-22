param(
  [switch]$SkipInstall
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$PidFile = Join-Path $PSScriptRoot ".surplussync-pids.json"
$LogDir = Join-Path $PSScriptRoot "logs"
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

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

  $stdout = Join-Path $LogDir "$Name.out.log"
  $stderr = Join-Path $LogDir "$Name.err.log"
  $fullCommand = "$envBlock$Command"
  $process = Start-Process -FilePath "powershell.exe" `
    -ArgumentList @("-NoProfile", "-Command", $fullCommand) `
    -WorkingDirectory $WorkingDirectory `
    -RedirectStandardOutput $stdout `
    -RedirectStandardError $stderr `
    -WindowStyle Hidden `
    -PassThru
  [pscustomobject]@{ name = $Name; pid = $process.Id; path = $WorkingDirectory; stdout = $stdout; stderr = $stderr }
}

function Wait-ForHttp {
  param(
    [string]$Name,
    [string]$Url,
    [object[]]$Processes,
    [int]$TimeoutSeconds = 90
  )

  $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
  while ((Get-Date) -lt $deadline) {
    foreach ($record in $Processes) {
      if (-not (Get-Process -Id $record.pid -ErrorAction SilentlyContinue)) {
        throw "$($record.name) exited early. See $($record.stdout) and $($record.stderr)."
      }
    }
    try {
      Invoke-RestMethod -Uri $Url -TimeoutSec 3 | Out-Null
      Write-Host "$Name ready at $Url"
      return
    } catch {
      Start-Sleep -Seconds 2
    }
  }
  throw "$Name did not become ready at $Url within $TimeoutSeconds seconds."
}

function Assert-PortAvailable {
  param([int]$Port)
  $listeners = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
  if (-not $listeners) { return }

  $details = $listeners | ForEach-Object {
    $pidValue = $_.OwningProcess
    $proc = Get-CimInstance Win32_Process -Filter "ProcessId=$pidValue" -ErrorAction SilentlyContinue
    "PID $pidValue $($proc.Name): $($proc.CommandLine)"
  }
  throw "Required port $Port is already in use. Stop the owning process first:`n$($details -join "`n")"
}

$mlDir = Join-Path $Root "services/ml-api"
$copilotDir = Join-Path $Root "services/copilot-api"
$webDir = Join-Path $Root "apps/web"

Assert-PortAvailable 8000
Assert-PortAvailable 3001
Assert-PortAvailable 3000

if (-not $SkipInstall) {
  if (-not (Test-Path (Join-Path $mlDir ".venv"))) {
    Push-Location $mlDir
    py -3.13 -m venv .venv
    .\.venv\Scripts\python.exe -m pip install --upgrade pip
    .\.venv\Scripts\python.exe -m pip install -e ".[dev]"
    Pop-Location
  }
  Push-Location $copilotDir
  if (-not (Test-Path "node_modules")) { npm ci }
  npm run build
  Pop-Location
  if (-not (Test-Path (Join-Path $webDir "node_modules"))) {
    Push-Location $webDir
    bun install --frozen-lockfile
    Pop-Location
  }
}

$token = "dev-local-main-app-token-change-me"
$copilotToken = $token

$processes = @()
$processes += Start-SurplusProcess -Name "ml" -WorkingDirectory $mlDir -Command ".\.venv\Scripts\python.exe -m uvicorn surplussync_ml.api.main:app --host 127.0.0.1 --port 8000" -Environment @{
  ALLOW_DEMO_FIXTURE = "true"
}
$processes += Start-SurplusProcess -Name "copilot" -WorkingDirectory $copilotDir -Command "npm start" -Environment @{
  NODE_ENV = "production"
  VITE_PROD = "true"
  PORT = "3001"
  ML_SERVICE_URL = "http://127.0.0.1:8000"
  MAIN_APP_SERVICE_TOKEN = $token
  COPILOT_ALLOW_FORECAST_FALLBACK = "true"
}
$processes += Start-SurplusProcess -Name "web" -WorkingDirectory $webDir -Command "bun run dev -- --host 127.0.0.1 --port 3000 --strictPort" -Environment @{
  ML_SERVICE_URL = "http://127.0.0.1:8000"
  COPILOT_SERVICE_URL = "http://127.0.0.1:3001"
  COPILOT_SERVICE_TOKEN = $copilotToken
  MAIN_APP_SERVICE_TOKEN = $token
  ALLOW_FORECAST_FALLBACK = "true"
}

$processes | ConvertTo-Json | Set-Content -Path $PidFile -Encoding UTF8

try {
  Wait-ForHttp -Name "ML API" -Url "http://127.0.0.1:8000/health" -Processes $processes
  Wait-ForHttp -Name "AI assistant" -Url "http://127.0.0.1:3001/health" -Processes $processes
  Wait-ForHttp -Name "Frontend" -Url "http://127.0.0.1:3000/api/forecast/health" -Processes $processes
} catch {
  Write-Host $_.Exception.Message
  Write-Host "Run .\scripts\stop.ps1 to stop any recorded processes."
  throw
}

Write-Host "SurplusSync Plus services ready."
Write-Host "ML API:        http://127.0.0.1:8000"
Write-Host "AI assistant:  http://127.0.0.1:3001"
Write-Host "Frontend:      http://127.0.0.1:3000"
if (-not $env:GEMINI_API_KEY) {
  Write-Host "GEMINI_API_KEY is not set; deterministic language fallback will be used."
}
Write-Host "PID file: $PidFile"
