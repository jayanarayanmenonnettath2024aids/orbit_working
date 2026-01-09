@echo off
echo ========================================
echo Orbit Setup - Installing Dependencies
echo ========================================
echo.
echo This will install all required dependencies for:
echo - Backend (Python packages)
echo - Frontend (Node.js packages)
echo.
echo Press Ctrl+C to cancel, or
pause
echo.

REM Check Python
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)
python --version
echo.

REM Check Node.js
echo [2/4] Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed or not in PATH!
    echo Please install Node.js 16 or higher from https://nodejs.org/
    pause
    exit /b 1
)
node --version
npm --version
echo.

REM Install Python dependencies
echo [3/4] Installing Python dependencies...
cd backend
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install Python dependencies!
    cd ..
    pause
    exit /b 1
)
cd ..
echo [OK] Python dependencies installed!
echo.

REM Install Node.js dependencies
echo [4/4] Installing Node.js dependencies...
cd frontend
npm install
if errorlevel 1 (
    echo [ERROR] Failed to install Node.js dependencies!
    cd ..
    pause
    exit /b 1
)
cd ..
echo [OK] Node.js dependencies installed!
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo You can now run the application using:
echo   - start-servers.bat (both servers)
echo   - start-backend.bat (backend only)
echo   - start-frontend.bat (frontend only)
echo.
pause
