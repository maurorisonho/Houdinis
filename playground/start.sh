#!/bin/bash

# ============================================
# Houdinis Playground - Quick Start Script
# ============================================

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE} Houdinis Playground - Quick Start${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}Docker is not installed.${NC}"
    echo "Please install Docker from: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${YELLOW}Docker Compose is not installed.${NC}"
    echo "Please install Docker Compose from: https://docs.docker.com/compose/install/"
    exit 1
fi

echo -e "${GREEN}${NC} Docker is ready"
echo ""

# Choose deployment method
echo "Select deployment method:"
echo "  1) Docker Compose (Recommended - includes Redis, Nginx)"
echo "  2) Docker Run (Simple - playground only)"
echo ""
read -p "Enter choice [1-2]: " choice

case $choice in
    1)
        echo ""
        echo -e "${BLUE}Starting with Docker Compose...${NC}"
        
        # Create .env file if it doesn't exist
        if [ ! -f .env ]; then
            echo -e "${YELLOW}Creating .env file...${NC}"
            cat > .env << 'EOF'
# Houdinis Playground Configuration
NODE_ENV=production
NEXT_PUBLIC_APP_NAME=Houdinis Playground
NEXT_PUBLIC_APP_VERSION=1.0.0
NEXT_PUBLIC_PYODIDE_VERSION=0.25.0

# Optional: Add your analytics ID
# NEXT_PUBLIC_ANALYTICS_ID=G-XXXXXXXXXX
EOF
            echo -e "${GREEN}${NC} Created .env file"
        fi
        
        # Start services
        docker-compose up -d
        
        echo ""
        echo -e "${GREEN}========================================${NC}"
        echo -e "${GREEN} Playground is starting!${NC}"
        echo -e "${GREEN}========================================${NC}"
        echo ""
        echo "Services:"
        echo "  - Playground: http://localhost:3000"
        echo "  - Redis: localhost:6379"
        echo "  - Nginx: http://localhost:80"
        echo ""
        echo "Check status:"
        echo "  docker-compose ps"
        echo ""
        echo "View logs:"
        echo "  docker-compose logs -f playground"
        echo ""
        echo "Stop services:"
        echo "  docker-compose down"
        ;;
        
    2)
        echo ""
        echo -e "${BLUE}Starting with Docker Run...${NC}"
        
        # Build image if not exists
        if ! docker images houdinis/playground:latest -q | grep -q .; then
            echo -e "${YELLOW}Building Docker image...${NC}"
            ./build-docker.sh
        fi
        
        # Run container
        docker run -d \
            --name houdinis-playground \
            -p 3000:3000 \
            -e NODE_ENV=production \
            -e NEXT_PUBLIC_APP_NAME="Houdinis Playground" \
            -e NEXT_PUBLIC_APP_VERSION="1.0.0" \
            houdinis/playground:latest
        
        echo ""
        echo -e "${GREEN}========================================${NC}"
        echo -e "${GREEN} Playground is running!${NC}"
        echo -e "${GREEN}========================================${NC}"
        echo ""
        echo "Access: http://localhost:3000"
        echo ""
        echo "View logs:"
        echo "  docker logs -f houdinis-playground"
        echo ""
        echo "Stop container:"
        echo "  docker stop houdinis-playground"
        echo "  docker rm houdinis-playground"
        ;;
        
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo -e "${BLUE}Waiting for services to be ready...${NC}"
sleep 5

# Health check
echo "Health check..."
for i in {1..30}; do
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        echo -e "${GREEN}${NC} Playground is ready!"
        echo ""
        echo -e "${GREEN} Open your browser: ${BLUE}http://localhost:3000${NC}"
        exit 0
    fi
    echo -n "."
    sleep 2
done

echo ""
echo -e "${YELLOW}Service is taking longer than expected to start.${NC}"
echo "Check logs with: docker-compose logs -f playground"
exit 0
