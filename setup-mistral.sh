#!/bin/bash
# Houdinis Framework - Local Mistral AI Setup Script
# Author: Mauro Risonho de Paula Assumpção aka firebitsbr
# License: MIT

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
cat << 'EOF'

   HOUDINIS + MISTRAL LOCAL AI - SETUP
  100% Free, Offline & Private Quantum Crypto Analysis

EOF

echo ""

# Check prerequisites
check_prereqs() {
    echo -e "${BLUE}[*] Checking prerequisites...${NC}"
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}[!] Docker not found. Install: https://docs.docker.com/get-docker/${NC}"
        exit 1
    fi
    echo -e "${GREEN}[+] Docker found: $(docker --version)${NC}"
    
    # Check NVIDIA Docker (optional)
    if command -v nvidia-smi &> /dev/null; then
        echo -e "${GREEN}[+] NVIDIA GPU detected: $(nvidia-smi --query-gpu=name --format=csv,noheader | head -1)${NC}"
        HAS_GPU=true
    else
        echo -e "${YELLOW}[!] No NVIDIA GPU detected. Will run on CPU (slower).${NC}"
        HAS_GPU=false
    fi
    
    # Check Ollama (for local install)
    if command -v ollama &> /dev/null; then
        echo -e "${GREEN}[+] Ollama found: $(ollama --version)${NC}"
        HAS_OLLAMA=true
    else
        echo -e "${YELLOW}[!] Ollama not found (needed for local install).${NC}"
        HAS_OLLAMA=false
    fi
    
    echo ""
}

# Install Ollama
install_ollama() {
    echo -e "${BLUE}[*] Installing Ollama...${NC}"
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        curl -fsSL https://ollama.ai/install.sh | sh
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo -e "${YELLOW}[!] On macOS, download from: https://ollama.ai/download${NC}"
        exit 1
    else
        echo -e "${RED}[!] Unsupported OS: $OSTYPE${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}[+] Ollama installed successfully!${NC}"
    echo ""
}

# Choose deployment mode
choose_mode() {
    echo -e "${BLUE}[?] Choose deployment mode:${NC}"
    echo "  1)  Docker (Recommended - All-in-one)"
    echo "  2)  Local Install (Python + Ollama)"
    echo "  3)   Custom (Manual setup)"
    echo ""
    
    read -p "Enter choice [1-3]: " choice
    
    case $choice in
        1)
            MODE="docker"
            ;;
        2)
            MODE="local"
            ;;
        3)
            MODE="custom"
            ;;
        *)
            echo -e "${RED}[!] Invalid choice. Using Docker.${NC}"
            MODE="docker"
            ;;
    esac
    
    echo ""
}

# Deploy with Docker
deploy_docker() {
    echo -e "${BLUE}[*] Deploying Houdinis + Mistral with Docker...${NC}"
    
    cd "$(dirname "$0")"
    
    # Build image
    echo -e "${BLUE}[*] Building Docker image...${NC}"
    docker build -f docker/Dockerfile.mistral -t houdinis-mistral:latest .
    
    # Start services
    echo -e "${BLUE}[*] Starting services...${NC}"
    
    if [ "$HAS_GPU" = true ]; then
        echo -e "${GREEN}[+] GPU support enabled${NC}"
        docker compose -f docker/docker-compose-mistral.yml up -d
    else
        echo -e "${YELLOW}[!] Running without GPU (CPU mode)${NC}"
        docker compose -f docker/docker-compose-mistral.yml up -d
    fi
    
    echo ""
    echo -e "${GREEN}[+] Docker deployment started!${NC}"
    echo ""
    echo -e "${BLUE}Waiting for Ollama to download Mistral model...${NC}"
    echo -e "${YELLOW}(This may take 5-10 minutes on first run - 4.1GB download)${NC}"
    echo ""
    
    # Show logs
    docker logs -f houdinis_mistral &
    LOG_PID=$!
    
    # Wait for model download
    echo -e "${BLUE}[*] Monitoring container logs (Ctrl+C to stop)...${NC}"
    sleep 5
    
    # Stop log follow after user interrupt
    trap "kill $LOG_PID 2>/dev/null" EXIT
    
    wait $LOG_PID
}

# Deploy locally
deploy_local() {
    echo -e "${BLUE}[*] Setting up local installation...${NC}"
    
    # Check if Ollama is installed
    if [ "$HAS_OLLAMA" = false ]; then
        echo -e "${YELLOW}[?] Ollama is not installed. Install now? (y/n)${NC}"
        read -p "> " install_choice
        
        if [[ $install_choice == "y" || $install_choice == "Y" ]]; then
            install_ollama
        else
            echo -e "${RED}[!] Ollama is required. Exiting.${NC}"
            exit 1
        fi
    fi
    
    # Start Ollama server
    echo -e "${BLUE}[*] Starting Ollama server...${NC}"
    if ! pgrep -x "ollama" > /dev/null; then
        ollama serve &
        OLLAMA_PID=$!
        echo -e "${GREEN}[+] Ollama server started (PID: $OLLAMA_PID)${NC}"
        sleep 3
    else
        echo -e "${GREEN}[+] Ollama is already running${NC}"
    fi
    
    # Pull Mistral model
    echo -e "${BLUE}[*] Checking Mistral model...${NC}"
    if ! ollama list | grep -q "mistral:7b-instruct"; then
        echo -e "${YELLOW}[*] Downloading Mistral 7B Instruct (4.1GB)...${NC}"
        ollama pull mistral:7b-instruct
        echo -e "${GREEN}[+] Model downloaded!${NC}"
    else
        echo -e "${GREEN}[+] Model already available${NC}"
    fi
    
    # Install Python dependencies
    echo -e "${BLUE}[*] Installing Python dependencies...${NC}"
    pip3 install --quiet langchain-community chromadb
    
    echo ""
    echo -e "${GREEN}[+] Local installation complete!${NC}"
    echo ""
}

# Show status and URLs
show_status() {
    echo ""
    echo ""
    echo -e "  ${GREEN} HOUDINIS + MISTRAL LOCAL AI - READY!${NC}"
    echo ""
    echo ""
    
    if [ "$MODE" = "docker" ]; then
        echo -e "${BLUE} Access Points:${NC}"
        echo "  • Web Terminal: http://localhost:7681"
        echo "  • Ollama API: http://localhost:11434"
        echo ""
        echo -e "${BLUE} Docker Commands:${NC}"
        echo "  • View logs: docker logs -f houdinis_mistral"
        echo "  • Open shell: docker exec -it houdinis_mistral bash"
        echo "  • Run agent: docker exec -it houdinis_mistral python3 -m langchain_agents.mistral_local_agent"
        echo "  • Stop: docker compose -f docker/docker-compose-mistral.yml down"
        echo ""
    else
        echo -e "${BLUE} Local Installation:${NC}"
        echo "  • Ollama API: http://localhost:11434"
        echo ""
        echo -e "${BLUE} Python Commands:${NC}"
        echo "  • Run agent: python3 langchain_agents/mistral_local_agent.py"
        echo "  • Stop Ollama: killall ollama"
        echo ""
    fi
    
    echo -e "${BLUE} Available Models:${NC}"
    if [ "$MODE" = "docker" ]; then
        docker exec houdinis_mistral ollama list 2>/dev/null || echo "  (Check logs for model status)"
    else
        ollama list
    fi
    
    echo ""
    echo -e "${BLUE} Documentation:${NC}"
    echo "  • Full Guide: docs/MISTRAL_LOCAL_GUIDE.md"
    echo "  • Examples: See guide for code samples"
    echo ""
    echo -e "${BLUE} Quick Test:${NC}"
    echo '  python3 -c "from langchain_agents.mistral_local_agent import MistralQuantumAgent; agent = MistralQuantumAgent(); print(agent.chat(\"Is RSA-2048 quantum-safe?\"))"'
    echo ""
    echo ""
    echo ""
}

# Main
main() {
    check_prereqs
    choose_mode
    
    case $MODE in
        docker)
            deploy_docker
            ;;
        local)
            deploy_local
            ;;
        custom)
            echo -e "${YELLOW}[*] Custom setup selected. Follow manual steps in docs/MISTRAL_LOCAL_GUIDE.md${NC}"
            exit 0
            ;;
    esac
    
    show_status
    
    echo -e "${GREEN} Setup complete! Happy hacking with Houdinis + Mistral!${NC}"
    echo ""
}

# Run
main
