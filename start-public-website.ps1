Write-Host "Starting DentHub Public Website..." -ForegroundColor Cyan
Write-Host ""
Write-Host "Server will run on: http://192.168.1.18:3000" -ForegroundColor Green
Write-Host "Also accessible at: http://localhost:3000" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

Set-Location -Path "c:\xampp\htdocs\Denthub\public-website"
python -m http.server 3000 --bind 192.168.1.18
