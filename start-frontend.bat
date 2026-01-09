@echo off
echo ========================================
echo Starting Frontend Server (Vite)
echo ========================================
echo.

cd frontend

REM Check if node_modules exists
if not exist "node_modules" (
    echo [!] Node modules not found. Installing...
    echo.
    npm install
    if errorlevel 1 (
        echo.
        echo [ERROR] Failed to install dependencies!
        echo Please run: npm install
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

echo Starting Vite server...
echo.
npm run dev
pause
