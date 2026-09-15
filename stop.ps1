# ==============================================================================
# Real Estate Lead Bot - Stop Services
# ==============================================================================
[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$ProjectRoot = $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "--------------------------------------------------" -ForegroundColor Cyan
Write-Host " Stopping Real Estate Lead Bot Services...        " -ForegroundColor Cyan
Write-Host "--------------------------------------------------" -ForegroundColor Cyan

try {
    $null = docker info 2>&1
} catch {
    Write-Host "Error: Docker is not running." -ForegroundColor Red
    exit 1
}

# Stop the containers safely
Write-Host "Stopping Docker Compose containers..." -ForegroundColor Gray
docker compose stop

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to stop Docker Compose stack cleanly." -ForegroundColor Red
    exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Services stopped safely." -ForegroundColor Green
Write-Host "Current service status:" -ForegroundColor Cyan
docker compose ps
Write-Host "--------------------------------------------------" -ForegroundColor Cyan
