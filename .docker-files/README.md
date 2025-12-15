# Docker Configuration Files

This directory contains Docker-related shell scripts for building and running the Houdinis framework in containers.

##  Contents

- **`build-docker.sh`** - Script to build Docker images for Houdinis
- **`docker-run.sh`** - Script to run Houdinis containers
- **`setup-docker.sh`** - Docker environment setup script

##  Usage

### Building Docker Images

```bash
# Build the Docker image
bash .docker-files/build-docker.sh
```

### Running Containers

```bash
# Run Houdinis in a Docker container
bash .docker-files/docker-run.sh
```

### Setup Docker Environment

```bash
# Setup Docker environment
bash .docker-files/setup-docker.sh
```

##  Main Docker Configuration

For complete Docker configuration including Dockerfile and docker-compose.yml, see:
- **`docker/`** directory in project root - Main Docker infrastructure
- **`playground/`** directory - Playground-specific Docker setup

##  Related Documentation

- [Docker README](../docker/README.md) - Complete Docker documentation
- [Playground Docker Guide](../playground/DOCKER.md) - Playground Docker setup

##  Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+ (for multi-container setups)
- Sufficient disk space for images (~2-5GB)

---

**Developed by:** Human Logic & Coding with AI Assistance (Claude Sonnet 4.5)
