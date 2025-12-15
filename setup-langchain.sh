#!/bin/bash
# Houdinis Framework - LangChain + MCP Quick Start
# Author: Mauro Risonho de Paula Assumpção aka firebitsbr
# Developed by: Human Logic & Coding with AI Assistance (Claude Sonnet 4.5)

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo ""
echo "     Houdinis Framework - LangChain + MCP Setup           "
echo "     Quantum Cryptography with AI Intelligence            "
echo ""
echo -e "${NC}"

# Check prerequisites
check_prereqs() {
    echo -e "\n${YELLOW}[1/5] Checking prerequisites...${NC}"
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}[!] Docker not found. Please install Docker first.${NC}"
        exit 1
    fi
    echo -e "${GREEN} Docker installed${NC}"
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${RED}[!] Docker Compose not found. Please install Docker Compose.${NC}"
        exit 1
    fi
    echo -e "${GREEN} Docker Compose installed${NC}"
    
    # Check Python (for local mode)
    if command -v python3 &> /dev/null; then
        echo -e "${GREEN} Python 3 installed${NC}"
    else
        echo -e "${YELLOW} Python 3 not found (OK if using Docker only)${NC}"
    fi
}

# Setup environment
setup_env() {
    echo -e "\n${YELLOW}[2/5] Setting up environment...${NC}"
    
    if [ ! -f .env ]; then
        echo -e "${BLUE}Creating .env from template...${NC}"
        cp .env.example .env
        echo -e "${GREEN} Created .env file${NC}"
        echo -e "${YELLOW} Please edit .env and add your API keys!${NC}"
        
        read -p "Do you want to edit .env now? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            ${EDITOR:-nano} .env
        fi
    else
        echo -e "${GREEN} .env file already exists${NC}"
    fi
    
    # Check for API keys
    if grep -q "your-.*-api-key-here" .env 2>/dev/null; then
        echo -e "${YELLOW} Warning: Default API keys detected in .env${NC}"
        echo -e "${YELLOW}  Please update with your actual keys before running!${NC}"
    fi
}

# Choose deployment mode
choose_mode() {
    echo -e "\n${YELLOW}[3/5] Choose deployment mode:${NC}"
    echo "1) Docker (Recommended - includes all services)"
    echo "2) Local (Python only - requires manual setup)"
    echo "3) Docker Minimal (Houdinis + MCP only)"
    
    read -p "Enter choice [1-3]: " mode
    
    case $mode in
        1)
            deploy_docker_full
            ;;
        2)
            deploy_local
            ;;
        3)
            deploy_docker_minimal
            ;;
        *)
            echo -e "${RED}Invalid choice. Exiting.${NC}"
            exit 1
            ;;
    esac
}

# Deploy full Docker stack
deploy_docker_full() {
    echo -e "\n${YELLOW}[4/5] Building Docker images...${NC}"
    docker-compose -f docker/docker-compose-langchain.yml build
    
    echo -e "\n${YELLOW}[5/5] Starting services...${NC}"
    docker-compose -f docker/docker-compose-langchain.yml up -d
    
    show_status
}

# Deploy minimal Docker
deploy_docker_minimal() {
    echo -e "\n${YELLOW}[4/5] Building minimal Docker image...${NC}"
    docker build -f docker/Dockerfile.langchain -t houdinis-langchain:latest .
    
    echo -e "\n${YELLOW}[5/5] Starting Houdinis container...${NC}"
    docker run -d \
        --name houdinis-langchain \
        --env-file .env \
        -p 7681:7681 -p 8000:8000 -p 8001:8001 \
        --gpus all \
        houdinis-langchain:latest
    
    show_status_minimal
}

# Deploy locally
deploy_local() {
    echo -e "\n${YELLOW}[4/5] Installing Python dependencies...${NC}"
    
    # Check if in virtual environment
    if [[ -z "${VIRTUAL_ENV}" ]]; then
        echo -e "${YELLOW}Not in a virtual environment. Creating one...${NC}"
        python3 -m venv venv
        source venv/bin/activate
    fi
    
    pip install -U pip setuptools wheel
    pip install -r requirements.txt
    pip install -r requirements-langchain.txt
    
    echo -e "\n${YELLOW}[5/5] Setup complete!${NC}"
    echo -e "${GREEN} Local environment ready${NC}"
    echo ""
    echo -e "${BLUE}To start the MCP server:${NC}"
    echo "  python -m mcp_servers.quantum_mcp_server"
    echo ""
    echo -e "${BLUE}To start the LangChain agent:${NC}"
    echo "  python -m langchain_agents.quantum_agent"
}

# Show service status
show_status() {
    echo ""
    echo -e "${GREEN}${NC}"
    echo -e "${GREEN}  Houdinis Framework with LangChain + MCP is running!    ${NC}"
    echo -e "${GREEN}${NC}"
    echo ""
    echo -e "${BLUE}Service URLs:${NC}"
    echo "  • Web Terminal:     http://localhost:7681"
    echo "  • MCP Server:       http://localhost:8000"
    echo "  • LangChain API:    http://localhost:8001"
    echo "  • ChromaDB:         http://localhost:8080"
    echo "  • MCP Gateway:      http://localhost:9000"
    echo ""
    echo -e "${BLUE}Useful Commands:${NC}"
    echo "  • View logs:        docker-compose -f docker/docker-compose-langchain.yml logs -f"
    echo "  • Stop services:    docker-compose -f docker/docker-compose-langchain.yml down"
    echo "  • Restart:          docker-compose -f docker/docker-compose-langchain.yml restart"
    echo ""
    echo -e "${BLUE}Access the agent:${NC}"
    echo "  docker exec -it houdinis_langchain python -m langchain_agents.quantum_agent"
    echo ""
    echo -e "${YELLOW}Documentation:${NC}"
    echo "  docs/LANGCHAIN_MCP_GUIDE.md"
    echo ""
}

# Show minimal status
show_status_minimal() {
    echo ""
    echo -e "${GREEN} Houdinis container started!${NC}"
    echo ""
    echo -e "${BLUE}Service URLs:${NC}"
    echo "  • Web Terminal:  http://localhost:7681"
    echo "  • MCP Server:    http://localhost:8000"
    echo "  • LangChain API: http://localhost:8001"
    echo ""
    echo -e "${BLUE}Access the agent:${NC}"
    echo "  docker exec -it houdinis-langchain python -m langchain_agents.quantum_agent"
    echo ""
}

# Main execution
main() {
    check_prereqs
    setup_env
    choose_mode
}

# Run main
main
