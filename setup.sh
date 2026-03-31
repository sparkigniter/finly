#!/bin/bash

# --- Color Configuration for UI ---
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color
INFO='\033[0;34m'

echo -e "${INFO}=== Finly Infrastructure Bootstrap Tool ===${NC}"

# --- Helper: Check and Install System Packages ---
check_and_install() {
    if ! command -v "$1" &> /dev/null; then
        echo -e "${RED}[!] $1 is not installed.${NC}"
        read -p "Would you like to install $1? (y/n): " confirm
        if [[ $confirm == [yY] ]]; then
            sudo apt update && sudo apt install -y "$2"
        else
            echo "Skipping $1. This might break the build."
        fi
    else
        echo -e "${GREEN}[✓] $1 is already installed.${NC}"
    fi
}

# 1. System Dependency Triage
check_and_install "python3" "python3-full"
check_and_install "pip3" "python3-pip"
check_and_install "node" "nodejs"
check_and_install "npm" "npm"

# 2. Python Backend Setup
echo -e "\n${INFO}--- Setting up Python Backend ---${NC}"
if [ -d "app/backend" ]; then
    cd app/backend
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
    fi
    source venv/bin/activate
    echo "Installing Python dependencies..."
    pip install -r requirements.txt
    cd ../..
else
    echo -e "${RED}Error: app/backend directory not found!${NC}"
fi

# 3. Node.js Frontend Setup
echo -e "\n${INFO}--- Setting up Frontend ---${NC}"
if [ -d "app/frontend" ]; then
    cd app/frontend
    echo "Installing NPM packages..."
    npm install
    cd ../..
else
    echo -e "${RED}Error: app/frontend directory not found!${NC}"
fi

# 4. Service Orchestration (Interactive)
echo -e "\n${INFO}=== Deployment Options ===${NC}"
echo "1) Run Backend Only"
echo "2) Run Frontend Only"
echo "3) Run Both (Background)"
echo "4) Exit"
read -p "Select an option: " choice

case $choice in
    1)
        source app/backend/venv/bin/activate && python3 -m app.backend.apis
        ;;
    2)
        cd app/frontend && npm run dev
        ;;
    3)
        echo "Starting services in background..."
        # Backend
        nohup bash -c "source app/backend/venv/bin/activate && python3 -m app.backend.apis" > backend.log 2>&1 &
        # Frontend
        nohup bash -c "cd app/frontend && npm run dev" > frontend.log 2>&1 &
        echo -e "${GREEN}Services are running. Check backend.log and frontend.log for output.${NC}"
        ;;
    *)
        echo "Exiting..."
        exit 0
        ;;
esac