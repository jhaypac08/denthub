# Quick Start Script
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "DentHub Employee Management System" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Prerequisites:" -ForegroundColor Yellow
Write-Host "1. Make sure XAMPP MySQL/MariaDB is running" -ForegroundColor White
Write-Host "2. Database 'denthub_db' should exist" -ForegroundColor White
Write-Host ""

Write-Host "Starting servers..." -ForegroundColor Green
Write-Host ""

Write-Host "Step 1: Start Backend (Django)" -ForegroundColor Cyan
Write-Host "Run in a new terminal: .\start-backend.ps1" -ForegroundColor White
Write-Host ""

Write-Host "Step 2: Start Frontend (Vue.js)" -ForegroundColor Cyan
Write-Host "Run in another terminal: .\start-frontend.ps1" -ForegroundColor White
Write-Host ""

Write-Host "Login Credentials:" -ForegroundColor Green
Write-Host "Username: admin" -ForegroundColor White
Write-Host "Password: admin123" -ForegroundColor White
Write-Host ""

Write-Host "Access Points:" -ForegroundColor Green
Write-Host "Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "Backend API: http://127.0.0.1:8000/api/" -ForegroundColor White
Write-Host "Django Admin: http://127.0.0.1:8000/admin/" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Do you want to start the backend now? (Y/N)"
if ($choice -eq "Y" -or $choice -eq "y") {
    .\start-backend.ps1
}
