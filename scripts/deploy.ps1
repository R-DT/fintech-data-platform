# ====================================================================
# FINTECH DATA PLATFORM - AUTOMATED ONE-CLICK INFRASTRUCTURE DEPLOYER
# ====================================================================
$ErrorActionPreference = "Stop"

Write-Host "🚀 Starting Fintech Data Platform deployment pipeline..." -ForegroundColor Cyan

# 1. Environment pre-flight integrity check
if (-not (Test-Path ".env")) {
    Write-Host "⚠️ Alert: Local active .env configuration file not found!" -ForegroundColor Yellow
    Write-Host "Creating .env from example template parameters..." -ForegroundColor Gray
    Copy-Item -Path ".env.example" -Destination ".env" -Force
}

# 2. Cycle terminal and clear stale container layers
Write-Host "🧹 Purging active legacy infrastructure caches..." -ForegroundColor Gray
docker compose -f docker/docker-compose.yml down -v --remove-orphans

# 3. Compile application image and launch the network stack
Write-Host "🏗️ Compiling multi-stage application image and standing up environment services..." -ForegroundColor Gray
docker compose -f docker/docker-compose.yml up --build -d

# 4. Success verification report
Write-Host "✨ Deployment Complete: Success!" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "👉 Database Container Name: fintech_warehouse_container" -ForegroundColor White
Write-Host "👉 Active Container Port Forward Routing Map: 5432:5432" -ForegroundColor White
Write-Host "👉 Application Execution Logs Tracker: docker logs fintech_pipeline_container" -ForegroundColor White
Write-Host "==========================================================" -ForegroundColor Green
