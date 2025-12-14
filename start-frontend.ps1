# Start Frontend Server
Write-Host "Starting Vue.js Frontend Server..." -ForegroundColor Green
Set-Location -Path "c:\xampp\htdocs\Denthub\frontend"

Write-Host "Frontend will start at http://192.168.1.18:5173" -ForegroundColor Yellow
Write-Host "Login: admin / admin123" -ForegroundColor Cyan
Write-Host ""

npm run dev -- --host 192.168.1.18
