#!/bin/bash
# Deploy Houdinis Framework com Mistral AI
# Autor: Mauro Risonho de Paula Assumpção

set -e

echo " Houdinis Framework - Deploy com Mistral AI"
echo "================================================"
echo ""

# Verificar se Docker está rodando
if ! docker ps > /dev/null 2>&1; then
    echo " Erro: Docker não está rodando"
    exit 1
fi

# Verificar se NVIDIA GPU está disponível
if command -v nvidia-smi &> /dev/null; then
    echo " NVIDIA GPU detectada:"
    nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader
    echo ""
else
    echo "  Aviso: NVIDIA GPU não detectada. Mistral será mais lento."
    echo ""
fi

# Escolher perfil
echo "Escolha o perfil de deployment:"
echo "1) LITE + Mistral AI (4 containers: Web UI + Core + Redis + Mistral)"
echo "2) FULL (6+ containers: todos os serviços)"
echo ""
read -p "Opção [1-2]: " PROFILE

cd "$(dirname "$0")"

case $PROFILE in
    1)
        echo ""
        echo " Iniciando build LITE + Mistral AI..."
        echo "   Containers: webui, houdinis-core, redis, mistral"
        echo ""
        
        # Build apenas se necessário
        echo "[1/4] Build Web UI..."
        docker compose -f docker/docker-compose-lite.yml build webui
        
        echo "[2/4] Build Houdinis Core..."
        docker compose -f docker/docker-compose-lite.yml build houdinis-core
        
        echo "[3/4] Build Mistral AI (pode levar 10-15 minutos)..."
        docker compose -f docker/docker-compose-lite.yml build mistral
        
        echo "[4/4] Iniciando containers..."
        docker compose -f docker/docker-compose-lite.yml up -d
        
        COMPOSE_FILE="docker/docker-compose-lite.yml"
        ;;
    2)
        echo ""
        echo " Iniciando build FULL..."
        docker compose -f docker/docker-compose.yml build
        docker compose -f docker/docker-compose.yml up -d
        COMPOSE_FILE="docker/docker-compose.yml"
        ;;
    *)
        echo " Opção inválida"
        exit 1
        ;;
esac

echo ""
echo "⏳ Aguardando containers ficarem saudáveis..."
sleep 10

# Verificar status
echo ""
echo " Status dos Containers:"
docker compose -f $COMPOSE_FILE ps

echo ""
echo " Deploy concluído!"
echo ""
echo ""
echo "   ACESSOS"
echo ""
echo ""
echo "  Web UI:           http://localhost:8080"
echo "  Login:            admin / houdinis123"
echo ""
echo "  Ollama API:       http://localhost:11434"
echo "  Mistral Terminal: http://localhost:7681 (se disponível)"
echo ""
echo ""
echo "   PRÓXIMOS PASSOS"
echo ""
echo ""
echo "  1. Acesse http://localhost:8080"
echo "  2. Faça login com: admin / houdinis123"
echo "  3. Vá para 'AI Assistant' no menu"
echo "  4. Aguarde o download do modelo Mistral (primeira vez)"
echo "     Tamanho: ~4.1GB, pode levar 5-10 minutos"
echo ""
echo ""
echo "    COMANDOS ÚTEIS"
echo ""
echo ""
echo "  Ver logs:         docker compose -f $COMPOSE_FILE logs -f"
echo "  Parar tudo:       docker compose -f $COMPOSE_FILE down"
echo "  Reiniciar:        docker compose -f $COMPOSE_FILE restart"
echo ""
echo "  Logs do Mistral:  docker logs houdinis_mistral -f"
echo "  Status GPU:       nvidia-smi"
echo ""
echo ""
echo ""
