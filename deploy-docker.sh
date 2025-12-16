#!/bin/bash
# Houdinis Framework - Complete Docker Deployment
# Author: Mauro Risonho de Paula Assumpção aka firebitsbr
# 100% Docker - ZERO local dependencies (except Docker itself)

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Banner
cat << 'EOF'

                                                                   
    HOUDINIS FRAMEWORK - COMPLETE DOCKER DEPLOYMENT             
                                                                   
   Quantum Cryptography Testing Platform                          
   100% Containerized - Zero Local Dependencies                   
                                                                   

EOF

echo ""
echo -e "${CYAN} Everything runs in Docker containers${NC}"
echo -e "${CYAN} Access via Web UI only${NC}"
echo -e "${CYAN} Your laptop stays clean!${NC}"
echo ""

# Check prerequisites (ONLY Docker)
check_prereqs() {
    echo -e "${BLUE}[1/6] Checking prerequisites...${NC}"
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}[!] Docker not found.${NC}"
        echo -e "${YELLOW}Install Docker: https://docs.docker.com/get-docker/${NC}"
        exit 1
    fi
    echo -e "${GREEN} Docker installed: $(docker --version | cut -d' ' -f3)${NC}"
    
    # Check Docker Compose
    if ! docker compose version &> /dev/null 2>&1; then
        echo -e "${RED}[!] Docker Compose not found.${NC}"
        echo -e "${YELLOW}Install Docker Compose V2${NC}"
        exit 1
    fi
    echo -e "${GREEN} Docker Compose installed: $(docker compose version | cut -d' ' -f4)${NC}"
    
    # Check if Docker daemon is running
    if ! docker info &> /dev/null; then
        echo -e "${RED}[!] Docker daemon is not running.${NC}"
        echo -e "${YELLOW}Start Docker service first.${NC}"
        exit 1
    fi
    echo -e "${GREEN} Docker daemon running${NC}"
    
    # Check NVIDIA Docker (optional for GPU)
    if command -v nvidia-smi &> /dev/null; then
        GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader | head -1)
        echo -e "${GREEN} NVIDIA GPU detected: ${GPU_NAME}${NC}"
        HAS_GPU=true
    else
        echo -e "${YELLOW} No NVIDIA GPU detected (CPU mode - slower but works)${NC}"
        HAS_GPU=false
    fi
    
    echo ""
}

# Select deployment profile
select_profile() {
    echo -e "${BLUE}[2/6] Select deployment profile:${NC}"
    echo ""
    echo "  1)  FULL STACK (Recommended)"
    echo "     • Houdinis Core + Web UI"
    echo "     • LangChain + MCP Gateway"
    echo "     • Mistral AI (Ollama)"
    echo "     • ChromaDB + Redis"
    echo "     • Nginx Reverse Proxy"
    echo "     • Target vulnerable system"
    echo ""
    echo "  2)  LITE (Core + Web UI Only)"
    echo "     • Houdinis Core + Web UI"
    echo "     • Essential services only"
    echo "     • Minimal resource usage"
    echo ""
    echo "  3)  AI POWERED (Core + AI)"
    echo "     • Houdinis Core + Web UI"
    echo "     • Mistral AI local"
    echo "     • LangChain agents"
    echo "     • No cloud APIs"
    echo ""
    echo "  4)  ENTERPRISE (All + Monitoring)"
    echo "     • Everything from FULL STACK"
    echo "     • Prometheus + Grafana"
    echo "     • ELK Stack (logs)"
    echo "     • Health checks"
    echo ""
    
    read -p "Enter choice [1-4] (default: 1): " choice
    choice=${choice:-1}
    
    case $choice in
        1) PROFILE="full" ;;
        2) PROFILE="lite" ;;
        3) PROFILE="ai" ;;
        4) PROFILE="enterprise" ;;
        *)
            echo -e "${YELLOW}Invalid choice. Using FULL STACK.${NC}"
            PROFILE="full"
            ;;
    esac
    
    echo -e "${GREEN} Profile selected: $(echo $PROFILE | tr '[:lower:]' '[:upper:]')${NC}"
    echo ""
}

# Setup environment variables
setup_env() {
    echo -e "${BLUE}[3/6] Setting up environment...${NC}"
    
    if [ ! -f .env ]; then
        echo -e "${YELLOW}Creating .env file from template...${NC}"
        cp .env.example .env
        
        echo -e "${CYAN}[?] Configure API keys now? (optional)${NC}"
        read -p "Edit .env file? [y/N]: " edit_env
        
        if [[ $edit_env == "y" || $edit_env == "Y" ]]; then
            ${EDITOR:-nano} .env
        else
            echo -e "${YELLOW} Skipped. You can edit .env later for AI features.${NC}"
        fi
    else
        echo -e "${GREEN} .env file exists${NC}"
    fi
    
    echo ""
}

# Build Docker images
build_images() {
    echo -e "${BLUE}[4/6] Building Docker images...${NC}"
    echo -e "${YELLOW}This may take 5-10 minutes on first run...${NC}"
    echo ""
    
    cd "$(dirname "$0")"
    
    case $PROFILE in
        "full")
            echo -e "${CYAN}Building all images...${NC}"
            docker compose -f docker/docker-compose-full.yml build --parallel
            ;;
        "lite")
            echo -e "${CYAN}Building lite images...${NC}"
            docker compose -f docker/docker-compose-lite.yml build
            ;;
        "ai")
            echo -e "${CYAN}Building AI images...${NC}"
            docker compose -f docker/docker-compose-ai.yml build
            ;;
        "enterprise")
            echo -e "${CYAN}Building enterprise images...${NC}"
            docker compose -f docker/docker-compose-enterprise.yml build --parallel
            ;;
    esac
    
    echo ""
    echo -e "${GREEN} Images built successfully!${NC}"
    echo ""
}

# Start services
start_services() {
    echo -e "${BLUE}[5/6] Starting services...${NC}"
    
    case $PROFILE in
        "full")
            docker compose -f docker/docker-compose-full.yml up -d
            ;;
        "lite")
            docker compose -f docker/docker-compose-lite.yml up -d
            ;;
        "ai")
            docker compose -f docker/docker-compose-ai.yml up -d
            ;;
        "enterprise")
            docker compose -f docker/docker-compose-enterprise.yml up -d
            ;;
    esac
    
    echo ""
    echo -e "${GREEN} All services started!${NC}"
    echo ""
    
    # Wait for services to be healthy
    echo -e "${YELLOW}Waiting for services to be ready...${NC}"
    sleep 10
}

# Display access information
show_info() {
    echo -e "${BLUE}[6/6] Deployment complete!${NC}"
    echo ""
    echo ""
    echo "                                                                   "
    echo -e "  ${GREEN} HOUDINIS FRAMEWORK IS RUNNING!${NC}                              "
    echo "                                                                   "
    echo ""
    echo ""
    echo -e "${CYAN} WEB ACCESS POINTS:${NC}"
    echo ""
    echo -e "  ${GREEN}Primary Web UI:${NC}        http://localhost:8080"
    echo -e "  ${BLUE}Username:${NC}              admin"
    echo -e "  ${BLUE}Password:${NC}              houdinis123 (change after first login)"
    echo ""
    
    case $PROFILE in
        "full"|"enterprise")
            echo -e "${CYAN} ADDITIONAL SERVICES:${NC}"
            echo ""
            echo -e "  Web Terminal (ttyd):   http://localhost:7681"
            echo -e "  MCP Gateway:           http://localhost:8000"
            echo -e "  LangChain API:         http://localhost:8001"
            echo -e "  ChromaDB:              http://localhost:8002"
            echo -e "  Ollama API:            http://localhost:11434"
            echo ""
            ;;
        "ai")
            echo -e "${CYAN} AI SERVICES:${NC}"
            echo ""
            echo -e "  Ollama API:            http://localhost:11434"
            echo -e "  LangChain API:         http://localhost:8001"
            echo ""
            ;;
    esac
    
    if [[ $PROFILE == "enterprise" ]]; then
        echo -e "${CYAN} MONITORING:${NC}"
        echo ""
        echo -e "  Grafana:               http://localhost:3000"
        echo -e "  Prometheus:            http://localhost:9090"
        echo -e "  Kibana (Logs):         http://localhost:5601"
        echo ""
    fi
    
    echo -e "${CYAN} DOCKER MANAGEMENT:${NC}"
    echo ""
    echo -e "  View logs:             ${YELLOW}docker compose -f docker/docker-compose-${PROFILE}.yml logs -f${NC}"
    echo -e "  Stop services:         ${YELLOW}docker compose -f docker/docker-compose-${PROFILE}.yml down${NC}"
    echo -e "  Restart services:      ${YELLOW}docker compose -f docker/docker-compose-${PROFILE}.yml restart${NC}"
    echo -e "  View status:           ${YELLOW}docker compose -f docker/docker-compose-${PROFILE}.yml ps${NC}"
    echo ""
    echo -e "${CYAN} DOCUMENTATION:${NC}"
    echo ""
    echo -e "  Quick Start:           ${YELLOW}docs/QUICKSTART.md${NC}"
    echo -e "  API Reference:         ${YELLOW}docs/API_REFERENCE.md${NC}"
    echo -e "  User Guide:            ${YELLOW}docs/USER_GUIDE.md${NC}"
    echo ""
    echo -e "${GREEN} Ready to hack! Open your browser to http://localhost:8080${NC}"
    echo ""
}

# Cleanup function
cleanup() {
    echo ""
    echo -e "${RED}[!] Interrupted. Cleaning up...${NC}"
    exit 1
}

trap cleanup INT TERM

# Main execution
main() {
    check_prereqs
    select_profile
    setup_env
    build_images
    start_services
    show_info
    
    echo -e "${BLUE}${NC}"
    echo -e "${GREEN} Houdinis Framework deployed successfully!${NC}"
    echo -e "${BLUE}${NC}"
    echo ""
}

# Run
main
