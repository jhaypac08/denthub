@echo off
echo Starting DentHub Frontend Server on Network...
echo.
echo Frontend will be accessible at: http://192.168.1.18:5173
echo Share this URL with beta testers on your network!
echo.
cd /d "%~dp0frontend"
npm run dev
pause
