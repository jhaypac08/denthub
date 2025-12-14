# Start Backend Server
Write-Host "Starting Django Backend Server..." -ForegroundColor Green
Set-Location -Path "c:\xampp\htdocs\Denthub\backend"

# Note: Activate virtual environment manually if needed
# .\venv\Scripts\Activate.ps1

Write-Host "Backend server will start at http://192.168.1.18:8000" -ForegroundColor Yellow
Write-Host "Admin panel at http://192.168.1.18:8000/admin" -ForegroundColor Yellow
Write-Host "Login: admin / admin123" -ForegroundColor Cyan
Write-Host ""

python manage.py runserver 192.168.1.18:8000
