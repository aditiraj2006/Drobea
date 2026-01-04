#!/bin/bash

echo "================================================="
echo "   Starting Drobea with Docker..."
echo "================================================="
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# --- Check Docker installation ---
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed or not running.${NC}"
    echo "Please install Docker and start it."
    exit 1
fi

# --- Check Docker Compose installation ---
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Error: Docker Compose is not available.${NC}"
    echo "You can install it via: sudo apt install docker-compose"
    exit 1
fi

# --- Optional: check for .env files ---
if [ ! -f "./backend/.env" ]; then
    echo -e "${YELLOW}Creating backend .env from template...${NC}"
    if [ -f "./backend/env.example" ]; then
        cp ./backend/env.example ./backend/.env
    else
        echo -e "${RED}Warning: backend/env.example not found!${NC}"
    fi
fi

if [ ! -f "./frontend/.env.local" ]; then
    echo -e "${YELLOW}Creating frontend .env.local file...${NC}"
    cat > ./frontend/.env.local << EOF
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=Drobea
VITE_APP_VERSION=1.0.0
EOF
fi

echo
echo -e "${BLUE}Building and starting all services...${NC}"
echo -e "${YELLOW}(This may take a few minutes on the first run)${NC}"
echo

# --- Start Docker services ---
docker-compose up --build

# --- After services start ---
echo
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✅ Drobea is running!${NC}"
echo -e "${GREEN}========================================${NC}"
echo
echo -e "${BLUE}Backend:${NC}   http://localhost:8000"
echo -e "${BLUE}Frontend:${NC}  http://localhost:3000"
echo -e "${BLUE}API Docs:${NC}  http://localhost:8000/docs"
echo -e "${BLUE}MongoDB:${NC}   localhost:27017"
echo
echo -e "${YELLOW}Press Ctrl+C to stop all services${NC}"
echo
