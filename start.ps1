# ==============================================================================
# Real Estate Lead Bot - Start Services
# ==============================================================================
[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$ProjectRoot = $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "--------------------------------------------------" -ForegroundColor Cyan
Write-Host " Starting Real Estate Lead Bot Services...       " -ForegroundColor Cyan
Write-Host "--------------------------------------------------" -ForegroundColor Cyan

# 1. Verify Docker daemon is responsive
try {
    $null = docker info 2>&1
} catch {
    Write-Host "Error: Docker is not running. Please launch Docker Desktop and try again." -ForegroundColor Red
    exit 1
}

# 2. Check for .env file presence (do not read or print contents)
if (-not (Test-Path "$ProjectRoot\.env")) {
    Write-Host "Warning: .env file not found in project root." -ForegroundColor Yellow
    if (Test-Path "$ProjectRoot\.env.example") {
        Write-Host "You can create one by copying .env.example to .env" -ForegroundColor Yellow
    }
}

# 3. Start containers in detached mode
Write-Host "Launching Docker Compose stack in detached mode..." -ForegroundColor Gray
docker compose up -d

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to start Docker Compose stack." -ForegroundColor Red
    exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Services started successfully!" -ForegroundColor Green
Write-Host "Current service status:" -ForegroundColor Cyan
docker compose ps

Write-Host ""
Write-Host "Available Endpoints:" -ForegroundColor Cyan
Write-Host "  - Frontend Chat UI : http://localhost:3000" -ForegroundColor White
Write-Host "  - Backend API Docs : http://localhost:8000/docs" -ForegroundColor White
Write-Host "  - n8n Editor       : http://localhost:5678" -ForegroundColor White
Write-Host "  - MySQL Database   : localhost:3307" -ForegroundColor White
Write-Host "--------------------------------------------------" -ForegroundColor Cyan
