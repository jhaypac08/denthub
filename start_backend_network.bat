@echo off
echo Starting DentHub Backend Server on Network...
echo.
echo Backend will be accessible at: http://192.168.1.18:8000
echo.
cd /d "%~dp0backend"
python manage.py runserver 192.168.1.18:8000
pause
