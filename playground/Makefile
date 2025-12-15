# ============================================
# Houdinis Playground - Makefile
# ============================================

.PHONY: help build run stop restart logs clean test deploy

# Variables
IMAGE_NAME := houdinis/playground
VERSION := 1.0.0
CONTAINER_NAME := houdinis-playground
PORT := 3000

# Colors
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[1;33m
NC := \033[0m

help: ## Show this help message
	@echo "$(BLUE)Houdinis Playground - Docker Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}'
	@echo ""

# ============================================
# Development Commands
# ============================================

install: ## Install dependencies
	@echo "$(BLUE)Installing dependencies...$(NC)"
	npm install
	@echo "$(GREEN)✓ Dependencies installed$(NC)"

dev: ## Start development server
	@echo "$(BLUE)Starting development server...$(NC)"
	npm run dev

build-next: ## Build Next.js application
	@echo "$(BLUE)Building Next.js application...$(NC)"
	npm run build
	@echo "$(GREEN)✓ Build complete$(NC)"

# ============================================
# Docker Commands
# ============================================

build: ## Build Docker image
	@echo "$(BLUE)Building Docker image...$(NC)"
	./build-docker.sh
	@echo "$(GREEN)✓ Image built: $(IMAGE_NAME):$(VERSION)$(NC)"

build-no-cache: ## Build Docker image without cache
	@echo "$(BLUE)Building Docker image (no cache)...$(NC)"
	docker build --no-cache -t $(IMAGE_NAME):$(VERSION) -t $(IMAGE_NAME):latest .
	@echo "$(GREEN)✓ Image built$(NC)"

run: ## Run playground container
	@echo "$(BLUE)Starting playground container...$(NC)"
	docker run -d \
		--name $(CONTAINER_NAME) \
		-p $(PORT):3000 \
		-e NODE_ENV=production \
		-e NEXT_PUBLIC_APP_NAME="Houdinis Playground" \
		$(IMAGE_NAME):$(VERSION)
	@echo "$(GREEN)✓ Container started: http://localhost:$(PORT)$(NC)"

stop: ## Stop playground container
	@echo "$(BLUE)Stopping container...$(NC)"
	@docker stop $(CONTAINER_NAME) 2>/dev/null || true
	@docker rm $(CONTAINER_NAME) 2>/dev/null || true
	@echo "$(GREEN)✓ Container stopped$(NC)"

restart: stop run ## Restart playground container

logs: ## Show container logs
	@docker logs -f $(CONTAINER_NAME)

shell: ## Open shell in running container
	@docker exec -it $(CONTAINER_NAME) sh

# ============================================
# Docker Compose Commands
# ============================================

up: ## Start all services with Docker Compose
	@echo "$(BLUE)Starting services with Docker Compose...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✓ Services started$(NC)"
	@echo "Access playground at: http://localhost:$(PORT)"

down: ## Stop all services
	@echo "$(BLUE)Stopping services...$(NC)"
	docker-compose down
	@echo "$(GREEN)✓ Services stopped$(NC)"

ps: ## Show running services
	@docker-compose ps

logs-all: ## Show logs for all services
	@docker-compose logs -f

restart-all: down up ## Restart all services

# ============================================
# Maintenance Commands
# ============================================

clean: ## Remove containers, images, and volumes
	@echo "$(YELLOW)Cleaning up Docker resources...$(NC)"
	@docker-compose down -v 2>/dev/null || true
	@docker stop $(CONTAINER_NAME) 2>/dev/null || true
	@docker rm $(CONTAINER_NAME) 2>/dev/null || true
	@docker rmi $(IMAGE_NAME):$(VERSION) 2>/dev/null || true
	@docker rmi $(IMAGE_NAME):latest 2>/dev/null || true
	@echo "$(GREEN)✓ Cleanup complete$(NC)"

prune: ## Remove all unused Docker resources
	@echo "$(YELLOW)Pruning unused Docker resources...$(NC)"
	docker system prune -af --volumes
	@echo "$(GREEN)✓ Prune complete$(NC)"

# ============================================
# Testing Commands
# ============================================

test: ## Run tests
	@echo "$(BLUE)Running tests...$(NC)"
	npm run test

test-e2e: ## Run end-to-end tests
	@echo "$(BLUE)Running E2E tests...$(NC)"
	npm run test:e2e

lint: ## Run linter
	@echo "$(BLUE)Running linter...$(NC)"
	npm run lint

type-check: ## Run TypeScript type check
	@echo "$(BLUE)Running type check...$(NC)"
	npm run type-check

# ============================================
# Deployment Commands
# ============================================

push: ## Push image to registry
	@echo "$(BLUE)Pushing image to registry...$(NC)"
	docker push $(IMAGE_NAME):$(VERSION)
	docker push $(IMAGE_NAME):latest
	@echo "$(GREEN)✓ Image pushed$(NC)"

pull: ## Pull image from registry
	@echo "$(BLUE)Pulling image from registry...$(NC)"
	docker pull $(IMAGE_NAME):$(VERSION)
	@echo "$(GREEN)✓ Image pulled$(NC)"

deploy-vercel: ## Deploy to Vercel
	@echo "$(BLUE)Deploying to Vercel...$(NC)"
	vercel --prod
	@echo "$(GREEN)✓ Deployed to Vercel$(NC)"

deploy-local: build up ## Build and deploy locally

# ============================================
# Info Commands
# ============================================

info: ## Show container info
	@echo "$(BLUE)Container Information:$(NC)"
	@echo "  Name: $(CONTAINER_NAME)"
	@echo "  Image: $(IMAGE_NAME):$(VERSION)"
	@echo "  Port: $(PORT)"
	@echo ""
	@echo "$(BLUE)Running Containers:$(NC)"
	@docker ps --filter name=$(CONTAINER_NAME) --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

inspect: ## Inspect container
	@docker inspect $(CONTAINER_NAME)

stats: ## Show container resource usage
	@docker stats $(CONTAINER_NAME)

# ============================================
# Quick Start
# ============================================

quick-start: build run ## Quick start: build and run
	@echo ""
	@echo "$(GREEN)========================================$(NC)"
	@echo "$(GREEN)🎉 Playground is ready!$(NC)"
	@echo "$(GREEN)========================================$(NC)"
	@echo ""
	@echo "Access: $(BLUE)http://localhost:$(PORT)$(NC)"
	@echo ""
	@echo "Useful commands:"
	@echo "  $(GREEN)make logs$(NC)     - View logs"
	@echo "  $(GREEN)make stop$(NC)     - Stop playground"
	@echo "  $(GREEN)make restart$(NC)  - Restart playground"
	@echo ""

# Default target
.DEFAULT_GOAL := help
