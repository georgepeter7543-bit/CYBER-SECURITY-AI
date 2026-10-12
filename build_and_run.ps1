# PETER CYBER SECURITY PROGRAM - PowerShell Unified Build & Run Script

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  PETER CYBER SECURITY PROGRAM - UNIFIED FULL-STACK LAUNCHER" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Compile React Frontend into app/ui/dist
Write-Host "`n[1/2] Compiling React Frontend (app/ui)..." -ForegroundColor Yellow
Push-Location -Path "$PSScriptRoot\app\ui"
npm run build
Pop-Location

# 2. Launch Flask Backend serving both API and Frontend
Write-Host "`n[2/2] Launching Python Server (app/main.py)..." -ForegroundColor Green
Push-Location -Path "$PSScriptRoot\app"
python main.py
Pop-Location
