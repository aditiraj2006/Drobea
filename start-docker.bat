@echo off
echo =================================================
echo   Starting Drobea with Docker...
echo =================================================
echo.

REM --- Check if Docker is installed and running ---
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not running or not installed.
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)

REM --- Check if docker-compose is available ---
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker Compose not found.
    echo Installing or enabling Docker Compose is required.
    pause
    exit /b 1
)

echo.
echo [INFO] Building and starting all Docker services...
docker-compose up --build
echo.

echo ========================================
echo Drobea is running!
echo ========================================
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo MongoDB:  localhost:27017
echo ----------------------------------------
echo Press Ctrl+C to stop all services
echo.
pause
