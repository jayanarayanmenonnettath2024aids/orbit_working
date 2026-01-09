@echo off
echo ========================================
echo Starting Orbit - AI Opportunity Intelligence
echo ========================================
echo.
echo Starting Backend and Frontend servers...
echo.

REM Start backend in new window
start "Orbit Backend (Flask)" cmd /k "cd /d "%~dp0" && start-backend.bat"

REM Wait 2 seconds before starting frontend
timeout /t 2 /nobreak >nul

REM Start frontend in new window
start "Orbit Frontend (Vite)" cmd /k "cd /d "%~dp0" && start-frontend.bat"

echo.
echo ========================================
echo Both servers are starting!
echo ========================================
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Close this window to continue...
timeout /t 5
exit
