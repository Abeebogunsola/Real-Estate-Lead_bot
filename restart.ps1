# ==============================================================================
# Real Estate Lead Bot - Restart Services
# ==============================================================================
[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$ProjectRoot = $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "--------------------------------------------------" -ForegroundColor Cyan
Write-Host " Restarting Real Estate Lead Bot Services...      " -ForegroundColor Cyan
Write-Host "--------------------------------------------------" -ForegroundColor Cyan

try {
    $null = docker info 2>&1
} catch {
    Write-Host "Error: Docker is not running. Please launch Docker Desktop and try again." -ForegroundColor Red
    exit 1
}

# Restart the containers
Write-Host "Restarting Docker Compose containers..." -ForegroundColor Gray
docker compose restart

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to restart Docker Compose stack." -ForegroundColor Red
    exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Services restarted successfully!" -ForegroundColor Green
Write-Host "Current service status:" -ForegroundColor Cyan
docker compose ps

Write-Host ""
Write-Host "Available Endpoints:" -ForegroundColor Cyan
Write-Host "  - Frontend Chat UI : http://localhost:3000" -ForegroundColor White
Write-Host "  - Backend API Docs : http://localhost:8000/docs" -ForegroundColor White
Write-Host "  - n8n Editor       : http://localhost:5678" -ForegroundColor White
Write-Host "  - MySQL Database   : localhost:3307" -ForegroundColor White
Write-Host "--------------------------------------------------" -ForegroundColor Cyan
