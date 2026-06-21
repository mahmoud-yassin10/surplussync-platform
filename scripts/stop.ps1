$ErrorActionPreference = "Stop"
$PidFile = Join-Path $PSScriptRoot ".surplussync-pids.json"

if (-not (Test-Path $PidFile)) {
  Write-Host "No SurplusSync PID file found. Nothing to stop."
  exit 0
}

$records = Get-Content -Raw $PidFile | ConvertFrom-Json
foreach ($record in $records) {
  $process = Get-Process -Id $record.pid -ErrorAction SilentlyContinue
  if ($process) {
    Write-Host "Stopping $($record.name) PID $($record.pid)"
    Stop-Process -Id $record.pid
  }
}

Remove-Item -LiteralPath $PidFile -Force
Write-Host "Stopped processes recorded by start.ps1."
