#!/bin/bash

# ============================================
# Houdinis Playground - Docker Build Script
# ============================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="houdinis/playground"
VERSION="${VERSION:-1.0.0}"
REGISTRY="${REGISTRY:-docker.io}"
PLATFORMS="${PLATFORMS:-linux/amd64,linux/arm64}"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Houdinis Playground - Docker Build${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Function to print colored messages
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

print_success "Docker is installed"

# Check if we're in the playground directory
if [ ! -f "package.json" ]; then
    print_error "package.json not found. Please run this script from the playground directory."
    exit 1
fi

print_success "Found package.json"

# Build arguments
BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
GIT_COMMIT=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")

print_info "Build Configuration:"
echo "  - Image: ${IMAGE_NAME}"
echo "  - Version: ${VERSION}"
echo "  - Build Date: ${BUILD_DATE}"
echo "  - Git Commit: ${GIT_COMMIT}"
echo ""

# Build the Docker image
print_info "Building Docker image..."

docker build \
    --build-arg BUILD_DATE="${BUILD_DATE}" \
    --build-arg VERSION="${VERSION}" \
    --build-arg GIT_COMMIT="${GIT_COMMIT}" \
    -t "${IMAGE_NAME}:${VERSION}" \
    -t "${IMAGE_NAME}:latest" \
    -f Dockerfile \
    .

if [ $? -eq 0 ]; then
    print_success "Docker image built successfully!"
else
    print_error "Docker build failed!"
    exit 1
fi

echo ""
print_info "Image Details:"
docker images "${IMAGE_NAME}" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"

echo ""
print_success "Build complete!"
echo ""
echo "Next steps:"
echo "  1. Test locally:"
echo "     ${GREEN}docker run -p 3000:3000 ${IMAGE_NAME}:${VERSION}${NC}"
echo ""
echo "  2. Use with Docker Compose:"
echo "     ${GREEN}docker-compose up -d${NC}"
echo ""
echo "  3. Push to registry:"
echo "     ${GREEN}docker push ${IMAGE_NAME}:${VERSION}${NC}"
echo "     ${GREEN}docker push ${IMAGE_NAME}:latest${NC}"
echo ""

# Optional: Build multi-platform images
if [ "$MULTI_PLATFORM" = "true" ]; then
    print_info "Building multi-platform images..."
    
    if ! docker buildx version &> /dev/null; then
        print_warning "Docker Buildx is not available. Skipping multi-platform build."
    else
        print_info "Creating buildx builder..."
        docker buildx create --use --name houdinis-builder || true
        
        print_info "Building for platforms: ${PLATFORMS}"
        docker buildx build \
            --platform "${PLATFORMS}" \
            --build-arg BUILD_DATE="${BUILD_DATE}" \
            --build-arg VERSION="${VERSION}" \
            --build-arg GIT_COMMIT="${GIT_COMMIT}" \
            -t "${IMAGE_NAME}:${VERSION}" \
            -t "${IMAGE_NAME}:latest" \
            --push \
            -f Dockerfile \
            .
        
        print_success "Multi-platform build complete!"
    fi
fi

exit 0
