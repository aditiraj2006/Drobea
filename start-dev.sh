#!/bin/bash

echo "Starting Drobea Development Environment..."
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed or not in PATH${NC}"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}Error: Node.js is not installed or not in PATH${NC}"
    exit 1
fi

echo -e "${BLUE}Setting up Backend...${NC}"
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating Python virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install backend dependencies
echo -e "${YELLOW}Installing backend dependencies...${NC}"
pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file from template...${NC}"
    cp env.example .env
    echo
    echo -e "${RED}IMPORTANT: Please configure your .env file with your API keys before continuing!${NC}"
    echo -e "${YELLOW}Required: MONGODB_URL, GEMINI_API_KEY, CLOUDINARY credentials${NC}"
    echo
    read -p "Press Enter to continue after configuring .env file..."
fi

# Start backend in background
echo -e "${GREEN}Starting Backend Server...${NC}"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

echo
echo -e "${BLUE}Setting up Frontend...${NC}"
cd ../frontend

# Install frontend dependencies
echo -e "${YELLOW}Installing frontend dependencies...${NC}"
npm install

# Check if .env.local exists
if [ ! -f ".env.local" ]; then
    echo -e "${YELLOW}Creating .env.local file...${NC}"
    cat > .env.local << EOF
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=Drobea
VITE_APP_VERSION=1.0.0
EOF
fi

# Start frontend
echo -e "${GREEN}Starting Frontend Server...${NC}"
npm run dev &
FRONTEND_PID=$!

echo
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Drobea is starting up!${NC}"
echo -e "${GREEN}========================================${NC}"
echo
echo -e "${BLUE}Backend:${NC} http://localhost:8000"
echo -e "${BLUE}Frontend:${NC} http://localhost:3000"
echo -e "${BLUE}API Docs:${NC} http://localhost:8000/docs"
echo

# Function to cleanup on exit
cleanup() {
    echo
    echo -e "${YELLOW}Shutting down servers...${NC}"
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo -e "${GREEN}Servers stopped.${NC}"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

echo -e "${YELLOW}Press Ctrl+C to stop all servers${NC}"
echo

# Wait for user to stop
wait
