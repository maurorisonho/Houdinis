#  Houdinis Playground - Docker Guide

> **Desenvolvido:** Lógica e Codificação por Humano e AI Assistida (Claude Sonnet 4.5)

Complete guide for running Houdinis Playground with Docker.

---

##  Quick Start

### Option 1: Using Make (Recommended)

```bash
# Show all available commands
make help

# Build and run (quickest way)
make quick-start

# Access playground
open http://localhost:3000
```

### Option 2: Using Scripts

```bash
# Interactive setup
./start.sh

# Or build manually
./build-docker.sh
docker run -p 3000:3000 houdinis/playground:latest
```

### Option 3: Using Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

##  Architecture

### Multi-Stage Dockerfile

```
Stage 1: Dependencies (deps)
  > Install production dependencies

Stage 2: Builder (builder)
  > Install all dependencies
  > Build Next.js application
  > Generate optimized bundles

Stage 3: Runner (runner)
  > Copy built files
  > Create non-root user
  > Expose port 3000
  > Health check endpoint
  > Start application
```

**Benefits:**
-  Small image size (~200MB)
-  Fast builds with layer caching
-  Security (non-root user)
-  Production-optimized

---

##  Build Configuration

### Environment Variables

```bash
# Application
NODE_ENV=production
NEXT_PUBLIC_APP_NAME=Houdinis Playground
NEXT_PUBLIC_APP_VERSION=1.0.0

# JupyterLite/Pyodide
NEXT_PUBLIC_PYODIDE_VERSION=0.25.0

# Optional Analytics
NEXT_PUBLIC_ANALYTICS_ID=G-XXXXXXXXXX
NEXT_PUBLIC_SENTRY_DSN=https://xxx@sentry.io/xxx

# Optional Rate Limiting
UPSTASH_REDIS_URL=redis://redis:6379
RATE_LIMIT_ENABLED=true
```

### Build Arguments

```bash
docker build \
  --build-arg VERSION=1.0.0 \
  --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
  --build-arg GIT_COMMIT=$(git rev-parse --short HEAD) \
  -t houdinis/playground:1.0.0 \
  .
```

---

##  Deployment Options

### Local Development

```bash
# Development mode (hot reload)
npm run dev

# Production build locally
npm run build
npm start
```

### Docker Run (Simple)

```bash
# Pull image from registry
docker pull houdinis/playground:latest

# Run container
docker run -d \
  --name houdinis-playground \
  -p 3000:3000 \
  -e NODE_ENV=production \
  -e NEXT_PUBLIC_APP_NAME="Houdinis Playground" \
  houdinis/playground:latest

# Access
curl http://localhost:3000
```

### Docker Compose (Production)

```yaml
# docker-compose.yml
services:
  playground:
    image: houdinis/playground:latest
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "--spider", "http://localhost:3000"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Kubernetes (Scalable)

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: houdinis-playground
spec:
  replicas: 3
  selector:
    matchLabels:
      app: playground
  template:
    metadata:
      labels:
        app: playground
    spec:
      containers:
      - name: playground
        image: houdinis/playground:1.0.0
        ports:
        - containerPort: 3000
        env:
        - name: NODE_ENV
          value: production
        resources:
          limits:
            memory: "1Gi"
            cpu: "1"
          requests:
            memory: "512Mi"
            cpu: "0.5"
        livenessProbe:
          httpGet:
            path: /api/health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /api/health
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: playground-service
spec:
  selector:
    app: playground
  ports:
  - port: 80
    targetPort: 3000
  type: LoadBalancer
```

---

##  Configuration

### Resource Limits

```yaml
# docker-compose.yml
services:
  playground:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 512M
```

### Health Checks

```dockerfile
# Dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/api/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"
```

### Logging

```bash
# View logs
docker logs -f houdinis-playground

# JSON logs
docker logs --format json houdinis-playground

# Tail last 100 lines
docker logs --tail 100 houdinis-playground
```

### Volumes (Persistent Storage)

```yaml
# docker-compose.yml
services:
  playground:
    volumes:
      # Code persistence
      - ./user-code:/app/user-code
      # Logs
      - ./logs:/app/logs
      # Cache
      - playground-cache:/app/.next/cache
```

---

##  Security Best Practices

### Non-Root User

```dockerfile
# Create user with specific UID/GID
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

USER nextjs
```

### Read-Only Filesystem

```bash
docker run -d \
  --read-only \
  --tmpfs /tmp \
  --tmpfs /app/.next/cache \
  houdinis/playground:latest
```

### Network Isolation

```bash
# Create custom network
docker network create houdinis-network

# Run with network
docker run -d \
  --network houdinis-network \
  --name playground \
  houdinis/playground:latest
```

### Secrets Management

```bash
# Using Docker secrets
echo "my-secret-key" | docker secret create api_key -

docker service create \
  --name playground \
  --secret api_key \
  houdinis/playground:latest
```

---

##  Monitoring

### Prometheus Metrics

```yaml
# docker-compose.yml
services:
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
```

### Grafana Dashboard

```yaml
# docker-compose.yml
services:
  grafana:
    image: grafana/grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

### Container Stats

```bash
# Real-time stats
docker stats houdinis-playground

# Export stats
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" > stats.txt
```

---

##  Testing

### Run Tests in Container

```bash
# Unit tests
docker run --rm houdinis/playground:latest npm test

# E2E tests
docker run --rm \
  -e CI=true \
  houdinis/playground:latest \
  npm run test:e2e
```

### Smoke Test

```bash
# Build and test
docker build -t test-image .
docker run -d --name test-container -p 3000:3000 test-image

# Wait for startup
sleep 10

# Test endpoint
curl -f http://localhost:3000 || exit 1

# Cleanup
docker rm -f test-container
```

---

##  Troubleshooting

### Container Won't Start

```bash
# Check logs
docker logs houdinis-playground

# Inspect container
docker inspect houdinis-playground

# Check events
docker events --filter container=houdinis-playground
```

### Port Already in Use

```bash
# Find process using port 3000
lsof -i :3000

# Kill process
kill -9 $(lsof -t -i:3000)

# Or use different port
docker run -p 3001:3000 houdinis/playground:latest
```

### Out of Memory

```bash
# Increase memory limit
docker run -m 2g houdinis/playground:latest

# Or in docker-compose.yml
services:
  playground:
    deploy:
      resources:
        limits:
          memory: 2G
```

### Build Failures

```bash
# Clear build cache
docker builder prune -a

# Build with no cache
docker build --no-cache -t houdinis/playground:latest .

# Check disk space
df -h
```

### Network Issues

```bash
# Test network
docker run --rm --network container:houdinis-playground alpine ping google.com

# Restart Docker daemon
sudo systemctl restart docker
```

---

##  Performance Optimization

### Layer Caching

```dockerfile
# Copy package files first
COPY package*.json ./
RUN npm ci

# Then copy source code
COPY . .
RUN npm run build
```

### Multi-Stage Build

```dockerfile
# Use alpine for smaller images
FROM node:18-alpine AS base

# Separate dependencies stage
FROM base AS deps
COPY package*.json ./
RUN npm ci --only=production

# Build stage
FROM base AS builder
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Runtime stage
FROM base AS runner
COPY --from=builder /app/.next ./.next
```

### Image Size

```bash
# Check image size
docker images houdinis/playground

# Analyze layers
docker history houdinis/playground:latest

# Use dive for detailed analysis
dive houdinis/playground:latest
```

---

##  Makefile Commands Reference

```bash
# Development
make install          # Install dependencies
make dev             # Start dev server
make build-next      # Build Next.js

# Docker
make build           # Build Docker image
make run             # Run container
make stop            # Stop container
make restart         # Restart container
make logs            # View logs
make shell           # Open shell

# Docker Compose
make up              # Start all services
make down            # Stop all services
make ps              # Show services
make logs-all        # All service logs

# Maintenance
make clean           # Remove containers/images
make prune           # Prune unused resources

# Testing
make test            # Run tests
make lint            # Run linter
make type-check      # Type check

# Deployment
make push            # Push to registry
make deploy-vercel   # Deploy to Vercel

# Info
make info            # Container info
make stats           # Resource usage

# Quick Start
make quick-start     # Build and run
```

---

##  Registry Management

### Docker Hub

```bash
# Login
docker login

# Tag image
docker tag houdinis/playground:latest username/playground:latest

# Push
docker push username/playground:latest

# Pull
docker pull username/playground:latest
```

### GitHub Container Registry

```bash
# Login
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Tag
docker tag houdinis/playground:latest ghcr.io/maurorisonho/playground:latest

# Push
docker push ghcr.io/maurorisonho/playground:latest
```

### Private Registry

```bash
# Tag for private registry
docker tag houdinis/playground:latest registry.company.com/playground:latest

# Push
docker push registry.company.com/playground:latest
```

---

##  CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/docker.yml
name: Docker Build and Push

on:
  push:
    branches: [main]
    paths:
      - 'playground/**'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: ./playground
          push: true
          tags: houdinis/playground:latest,houdinis/playground:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

---

##  Cost Optimization

### Cloud Hosting Costs

**Docker Hub:**
- Free: 1 repository, 200 pulls/6h
- Pro: $5/month - Unlimited repositories

**DigitalOcean Droplet:**
- Basic: $6/month (1GB RAM, 1 vCPU)
- Standard: $12/month (2GB RAM, 1 vCPU)

**AWS ECS Fargate:**
- 0.5 vCPU, 1GB RAM: ~$15/month
- 1 vCPU, 2GB RAM: ~$30/month

**Azure Container Instances:**
- 1 vCPU, 1.5GB RAM: ~$35/month
- 2 vCPU, 4GB RAM: ~$70/month

---

##  Support

- **Documentation**: https://docs.houdinis.dev
- **Issues**: https://github.com/maurorisonho/Houdinis/issues
- **Discord**: https://discord.gg/houdinis

---

**Built with  for the quantum cryptanalysis community**
