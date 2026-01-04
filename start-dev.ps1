# start-dev.ps1
Write-Host "Starting Drobea Development Environment..." -ForegroundColor Cyan
Write-Host ""

# --- Define colors ---
$RED = "Red"
$GREEN = "Green"
$YELLOW = "Yellow"
$BLUE = "Blue"

# --- Check if Python is installed ---
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor $GREEN
} catch {
    Write-Host "Error: Python is not installed or not in PATH" -ForegroundColor $RED
    exit 1
}

# --- Check if Node.js is installed ---
try {
    $nodeVersion = node --version 2>&1
    Write-Host "Node.js found: $nodeVersion" -ForegroundColor $GREEN
} catch {
    Write-Host "Error: Node.js is not installed or not in PATH" -ForegroundColor $RED
    exit 1
}

# --- Backend setup ---
Write-Host "`nSetting up Backend..." -ForegroundColor $BLUE
Set-Location "backend"

if (-not (Test-Path "venv")) {
    Write-Host "Creating Python virtual environment..." -ForegroundColor $YELLOW
    python -m venv venv
}

Write-Host "Activating virtual environment..." -ForegroundColor $YELLOW
& ".\venv\Scripts\Activate.ps1"

Write-Host "Installing backend dependencies..." -ForegroundColor $YELLOW
pip install -r requirements.txt

if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file from template..." -ForegroundColor $YELLOW
    Copy-Item "env.example" ".env"
    Write-Host ""
    Write-Host "IMPORTANT: Configure your .env file before continuing!" -ForegroundColor $RED
    Write-Host "Required: MONGODB_URL, GEMINI_API_KEY, CLOUDINARY credentials" -ForegroundColor $YELLOW
    Write-Host ""
    Read-Host "Press Enter to continue after configuring .env file"
}

# --- Start backend ---
Write-Host "Starting Backend Server..." -ForegroundColor $GREEN
$backendJob = Start-Job -ScriptBlock {
    & uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
}

Start-Sleep -Seconds 3

# --- Frontend setup ---
Write-Host "`nSetting up Frontend..." -ForegroundColor $BLUE
Set-Location "..\frontend"

Write-Host "Installing frontend dependencies..." -ForegroundColor $YELLOW
npm install

if (-not (Test-Path ".env.local")) {
    Write-Host "Creating .env.local file..." -ForegroundColor $YELLOW
    @"
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=Drobea
VITE_APP_VERSION=1.0.0
"@ | Out-File -FilePath ".env.local" -Encoding UTF8
}

Write-Host "Starting Frontend Server..." -ForegroundColor $GREEN
$frontendJob = Start-Job -ScriptBlock {
    & npm run dev
}

Write-Host ""
Write-Host "========================================" -ForegroundColor $GREEN
Write-Host "Drobea is starting up!" -ForegroundColor $GREEN
Write-Host "========================================" -ForegroundColor $GREEN
Write-Host ""
Write-Host "Backend:  http://localhost:8000" -ForegroundColor $BLUE
Write-Host "Frontend: http://localhost:3000" -ForegroundColor $BLUE
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor $BLUE
Write-Host ""
Write-Host "Press Ctrl+C to stop all servers." -ForegroundColor $YELLOW
Write-Host ""

# --- Cleanup function ---
$cleanup = {
    Write-Host "`nShutting down servers..." -ForegroundColor $YELLOW
    if ($backendJob) { Stop-Job $backendJob -Force; Remove-Job $backendJob }
    if ($frontendJob) { Stop-Job $frontendJob -Force; Remove-Job $frontendJob }
    Write-Host "Servers stopped." -ForegroundColor $GREEN
    exit
}

# --- Trap Ctrl+C ---
Register-EngineEvent PowerShell.Exiting -Action { & $cleanup } | Out-Null
trap [System.Exception] { & $cleanup }

# --- Wait until user stops the script ---
while ($true) { Start-Sleep -Seconds 1 }
