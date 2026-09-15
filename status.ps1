# ==============================================================================
# Real Estate Lead Bot - Service Status & Health Check
# ==============================================================================
[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$ProjectRoot = $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "--------------------------------------------------" -ForegroundColor Cyan
Write-Host " Real Estate Lead Bot - Service Status            " -ForegroundColor Cyan
Write-Host "--------------------------------------------------" -ForegroundColor Cyan

try {
    $null = docker info 2>&1
} catch {
    Write-Host "Error: Docker daemon is not running." -ForegroundColor Red
    exit 1
}

Write-Host "Docker Compose Containers:" -ForegroundColor Cyan
docker compose ps

Write-Host ""
Write-Host "Checking Service Health & Endpoints..." -ForegroundColor Cyan

# 1. Frontend check
try {
    $frontendResp = Invoke-WebRequest -Uri "http://localhost:3000" -Method Head -TimeoutSec 3 -UseBasicParsing -ErrorAction Stop
    Write-Host "  [OK] Frontend UI   : http://localhost:3000 (HTTP $($frontendResp.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "  [--] Frontend UI   : http://localhost:3000 (Unreachable or starting)" -ForegroundColor Yellow
}

# 2. Backend API check
try {
    $backendResp = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/health" -Method Get -TimeoutSec 3 -UseBasicParsing -ErrorAction Stop
    Write-Host "  [OK] Backend API   : http://localhost:8000/docs (HTTP $($backendResp.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "  [--] Backend API   : http://localhost:8000 (Unreachable or starting)" -ForegroundColor Yellow
}

# 3. n8n Editor check
try {
    $n8nResp = Invoke-WebRequest -Uri "http://localhost:5678" -Method Head -TimeoutSec 3 -UseBasicParsing -ErrorAction Stop
    Write-Host "  [OK] n8n Workflow  : http://localhost:5678 (HTTP $($n8nResp.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "  [--] n8n Workflow  : http://localhost:5678 (Unreachable or starting)" -ForegroundColor Yellow
}

# 4. MySQL check
$mysqlContainer = docker compose ps -q mysql 2>$null
if ($mysqlContainer) {
    $mysqlHealth = docker inspect --format '{{.State.Health.Status}}' $mysqlContainer 2>$null
    if ($mysqlHealth -eq "healthy") {
        Write-Host "  [OK] MySQL Database: localhost:3307 (Status: healthy)" -ForegroundColor Green
    } elseif ($mysqlHealth) {
        Write-Host "  [--] MySQL Database: localhost:3307 (Status: $mysqlHealth)" -ForegroundColor Yellow
    } else {
        Write-Host "  [OK] MySQL Database: localhost:3307 (Running)" -ForegroundColor Green
    }
} else {
    Write-Host "  [--] MySQL Database: Not running" -ForegroundColor Red
}

Write-Host "--------------------------------------------------" -ForegroundColor Cyan
