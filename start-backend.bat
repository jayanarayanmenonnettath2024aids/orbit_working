@echo off
echo ========================================
echo Starting Backend Server (Flask)
echo ========================================
echo.

cd backend

REM Check if dependencies are installed
echo Checking Python dependencies...
python -c "import flask_cors" 2>nul
if errorlevel 1 (
    echo.
    echo [!] Dependencies not found. Installing...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo [ERROR] Failed to install dependencies!
        echo Please run: pip install -r backend\requirements.txt
        echo.
        pause
        exit /b 1
    )
    echo.
    echo [OK] Dependencies installed successfully!
    echo.
) else (
    echo [OK] Dependencies already installed.
    echo.
)

echo Starting Flask server...
echo.
python app.py
pause
