$ErrorActionPreference = "Stop"

function Assert-Equal {
  param($Actual, $Expected, [string]$Label)
  if ($Actual -ne $Expected) {
    throw "$Label expected $Expected but got $Actual"
  }
}

function Invoke-JsonPost {
  param([string]$Uri, [string]$Path)
  $body = Get-Content -Raw $Path
  Invoke-RestMethod -Uri $Uri -Method Post -ContentType "application/json" -Body $body
}

$Root = Split-Path -Parent $PSScriptRoot
$ml = "http://127.0.0.1:8000"
$copilot = "http://127.0.0.1:3001"
$frontend = "http://127.0.0.1:3000"

Write-Host "Checking ML health..."
$health = Invoke-RestMethod "$ml/health"
if ($health.status -ne "ok" -or $health.modelLoaded -ne $true) {
  throw "ML health did not report status ok with modelLoaded=true"
}

$baseline = Invoke-JsonPost "$ml/v1/forecast" (Join-Path $Root "services/ml-api/examples/canonical_request.json")
Assert-Equal $baseline.expectedAttendance 528 "baseline expectedAttendance"
Assert-Equal $baseline.intervalLow 497 "baseline intervalLow"
Assert-Equal $baseline.intervalHigh 557 "baseline intervalHigh"
Assert-Equal $baseline.recommendedPrep 562 "baseline recommendedPrep"
Assert-Equal $baseline.preventableSurplus 168 "baseline preventableSurplus"

$whatIf = Invoke-JsonPost "$ml/v1/what-if" (Join-Path $Root "services/ml-api/examples/what_if_request.json")
Assert-Equal $whatIf.expectedAttendance 540 "what-if expectedAttendance"
Assert-Equal $whatIf.intervalLow 512 "what-if intervalLow"
Assert-Equal $whatIf.intervalHigh 568 "what-if intervalHigh"
Assert-Equal $whatIf.recommendedPrep 575 "what-if recommendedPrep"
Assert-Equal $whatIf.preventableSurplus 155 "what-if preventableSurplus"

Write-Host "Checking Copilot health..."
$copilotHealth = Invoke-RestMethod "$copilot/health"
if ($copilotHealth.status -ne "ok") {
  throw "Copilot health did not report ok"
}
Write-Host "Copilot persistence mode: $($copilotHealth.sessionPersistence)"

Write-Host "Checking frontend forecast health..."
$frontendHealth = Invoke-RestMethod "$frontend/api/forecast/health"
if ($frontendHealth.mlServiceReachable -ne $true -or $frontendHealth.mlModelLoaded -ne $true) {
  throw "Frontend forecast health is not using live ML"
}
Write-Host "Frontend forecast health: $($frontendHealth.status), live ML reachable: $($frontendHealth.mlServiceReachable), fallback enabled: $($frontendHealth.fallbackEnabled)"

Write-Host "Canonical verification passed with live ML values."
