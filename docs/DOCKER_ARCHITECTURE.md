#  Arquitetura 100% Docker do Houdinis Framework

##  Índice

1. [Overview](#visão-geral)
2. [Arquitetura](#arquitetura)
3. [Componentes](#componentes)
4. [Perfis de Deployment](#perfis-de-deployment)
5. [Quick Start](#quick-start)
6. [Gestão de Containers](#gestão-de-containers)
7. [Segurança](#segurança)
8. [FAQ](#faq)

---

##  Overview

**Houdinis Framework agora roda 100% em Docker containers.**

###  O que MUDOU:

**ANTES (versão 1.x):**
```
 Usuário instala Python localmente
 Usuário instala Ollama localmente  
 Usuário executa scripts Python no laptop
 Dependências bagunçam o sistema
 Configurações complexas
```

**AGORA (versão 2.0):**
```
 ZERO instalações locais (só Docker)
 Tudo roda em containers isolados
 Usuário acessa apenas Web UI (porta 8080)
 Sistema limpo e organizado
 Deploy em 1 comando
```

---

##  Arquitetura

### Diagrama de Componentes

```

  USER (Browser)                                                 
                                                                 
      http://localhost:8080                                     
                                                                 
                                                                 
    
    WEB UI CONTAINER (Flask)                                  
    • Interface gráfica                                       
    • Autenticação                                            
    • Seleção de exploits                                     
    • Monitoramento                                           
    
                                                                 
      Docker Socket (controle)                                  
                                                                 
                                                                 
    
    BACKEND CONTAINERS                                        
                                                                
                      
     Houdinis Core      Mistral AI                       
     • Exploits         • LLM Local                      
     • Scanners         • RAG                            
     • Quantum          • Ollama                         
                      
                                                                
                      
     ChromaDB           Redis                            
     • Vector Store     • Cache                          
     • Embeddings       • Queue                          
                      
                                                                
                      
     MCP Gateway        Target System                    
     • AI Protocol      • Vulnerable                     
                      
                                                                
    
                                                                 
  Rede Interna Docker: 172.20.0.0/16                            
  (Containers se comunicam internamente)                        

```

### Fluxo de Dados

```
1. User abre http://localhost:8080 no browser
2. Web UI autentica usuário
3. User seleciona exploit (ex: Shor's RSA)
4. Web UI envia comando para Houdinis Core container
5. Houdinis Core executa exploit (internamente)
6. Resultados salvos em volume Docker
7. Web UI exibe resultados em tempo real
```

---

##  Componentes

### 1. **Web UI Container** (ÚNICO ponto de acesso)

**Imagem:** `houdinis-webui:latest`  
**Porta:** `8080` (exposta ao host)  
**Tecnologia:** Flask + Flask-SocketIO  
**Função:** Interface web para usuários

**Features:**
-  Dashboard com status de containers
-  Seleção de exploits
-  Chat com AI assistant (Mistral)
-  Configuração de backends quânticos
-  Visualização de resultados
-  Monitoramento em tempo real

**Acesso:**
```bash
http://localhost:8080
Username: admin
Password: houdinis123 (trocar após primeiro login)
```

---

### 2. **Houdinis Core Container**

**Imagem:** `houdinis-core:latest`  
**Porta:** Interna (não exposta)  
**Tecnologia:** Python 3.11 + CUDA  
**Função:** Engine de exploits quânticos

**Conteúdo:**
- `/opt/houdinis/exploits/` - Exploits quânticos
- `/opt/houdinis/scanners/` - Scanners de rede
- `/opt/houdinis/quantum/` - Backends quânticos
- `/opt/houdinis/results/` - Resultados salvos

**GPU Support:**
-  NVIDIA CUDA 12.4.1
-  cuQuantum para simulação
-  Até 40 qubits práticos

---

### 3. **Mistral AI Container** (Opcional)

**Imagem:** `houdinis-mistral:latest`  
**Porta:** `11434` (interna)  
**Tecnologia:** Ollama + Mistral 7B  
**Função:** AI assistant local (sem cloud)

**Features:**
-  Chat sobre quantum crypto
-  Geração de exploits
-  Análise de vulnerabilidades
-  100% offline e grátis

**Modelos Disponíveis:**
- `mistral:7b-instruct` (4.1GB) - General
- `codellama:13b-instruct` (7.3GB) - Code

---

### 4. **ChromaDB Container** (Opcional)

**Imagem:** `chromadb/chroma:latest`  
**Porta:** `8000` (interna)  
**Função:** Vector database para RAG

**Uso:**
- Indexação de documentação Houdinis
- Busca semântica local
- Embeddings via Ollama

---

### 5. **Redis Container**

**Imagem:** `redis:7-alpine`  
**Porta:** `6379` (interna)  
**Função:** Cache, sessões, job queue

**Uso:**
- Sessões do Web UI
- Queue de jobs (exploits)
- Cache de resultados

---

### 6. **MCP Gateway Container** (Opcional)

**Imagem:** `houdinis-mcp:latest`  
**Porta:** `8000` (interna)  
**Função:** Model Context Protocol server

**Tools Expostos:**
- `shor_factorize`
- `grover_bruteforce`
- `quantum_vulnerability_scan`
- `pqc_migration_advisor`

---

### 7. **Target Container** (Opcional)

**Imagem:** `ubuntu:22.04`  
**Porta:** `22` (SSH interno)  
**Função:** Sistema vulnerável para testes

**Serviços:**
- SSH com senha fraca
- TLS com RSA-2048
- Certificados auto-assinados

---

##  Perfis de Deployment

### 1. FULL STACK (Recomendado)

**Arquivo:** `docker-compose-full.yml`

**Inclui:**
-  Web UI
-  Houdinis Core
-  Mistral AI
-  ChromaDB
-  Redis
-  MCP Gateway
-  Target System

**Uso de Recursos:**
- CPU: 8+ cores
- RAM: 16GB+
- GPU: NVIDIA com 8GB+ VRAM
- Disk: 30GB+

**Deploy:**
```bash
./deploy-docker.sh
# Escolha opção 1 (FULL STACK)
```

---

### 2. LITE

**Arquivo:** `docker-compose-lite.yml`

**Inclui:**
-  Web UI
-  Houdinis Core
-  Redis

**Uso de Recursos:**
- CPU: 4+ cores
- RAM: 8GB
- GPU: Opcional
- Disk: 10GB

**Deploy:**
```bash
./deploy-docker.sh
# Escolha opção 2 (LITE)
```

**Ideal para:**
- Testes rápidos
- Ambientes com poucos recursos
- Desenvolvimento

---

### 3. AI POWERED

**Arquivo:** `docker-compose-ai.yml`

**Inclui:**
-  Web UI
-  Houdinis Core
-  Mistral AI
-  ChromaDB
-  Redis

**Uso de Recursos:**
- CPU: 6+ cores
- RAM: 12GB
- GPU: NVIDIA (recomendado)
- Disk: 20GB

**Deploy:**
```bash
./deploy-docker.sh
# Escolha opção 3 (AI POWERED)
```

**Ideal para:**
- Análise com IA sem cloud
- Ambientes offline/air-gapped
- Privacidade máxima

---

### 4. ENTERPRISE (Avançado)

**Arquivo:** `docker-compose-enterprise.yml`

**Inclui tudo de FULL + :**
-  Prometheus (métricas)
-  Grafana (dashboards)
-  ELK Stack (logs)
-  Alertmanager

**Uso de Recursos:**
- CPU: 12+ cores
- RAM: 32GB+
- GPU: NVIDIA com 16GB VRAM
- Disk: 100GB+

**Deploy:**
```bash
./deploy-docker.sh
# Escolha opção 4 (ENTERPRISE)
```

---

##  Quick Start

### Pré-requisitos

**APENAS Docker é necessário:**

```bash
# Check Docker
docker --version
# Docker version 24.0+ required

# Check Docker Compose
docker compose version
# Docker Compose version 2.20+ required

# Check GPU (opcional mas recomendado)
nvidia-smi
```

### Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/maurorisonho/Houdinis.git
cd Houdinis

# 2. Execute o deploy script
./deploy-docker.sh

# 3. Selecione perfil (1-4)
# Recomendado: 1 (FULL STACK)

# 4. Aguarde build (5-10 minutos na primeira vez)

# 5. Acesse Web UI
# http://localhost:8080
```

### Primeiro Login

```
URL: http://localhost:8080
Username: admin
Password: houdinis123

 TROQUE A SENHA após primeiro login!
```

---

##  Gestão de Containers

### Ver Status

```bash
# Full stack
docker compose -f docker/docker-compose-full.yml ps

# Lite
docker compose -f docker/docker-compose-lite.yml ps

# AI
docker compose -f docker/docker-compose-ai.yml ps
```

### Ver Logs

```bash
# Todos os containers
docker compose -f docker/docker-compose-full.yml logs -f

# Container específico
docker logs -f houdinis_webui
docker logs -f houdinis_core
docker logs -f houdinis_mistral
```

### Parar Serviços

```bash
docker compose -f docker/docker-compose-full.yml down
```

### Reiniciar Serviços

```bash
docker compose -f docker/docker-compose-full.yml restart
```

### Atualizar Imagens

```bash
# Rebuild all
docker compose -f docker/docker-compose-full.yml build --no-cache

# Restart
docker compose -f docker/docker-compose-full.yml up -d
```

### Limpar Tudo

```bash
# Stop e remove containers
docker compose -f docker/docker-compose-full.yml down -v

# Remove imagens
docker rmi houdinis-webui houdinis-core houdinis-mistral

# Remove volumes ( perde dados!)
docker volume prune
```

---

##  Segurança

### Isolamento de Containers

 **Cada container roda isolado**
- Rede interna Docker (172.20.0.0/16)
- Sem acesso direto ao host
- Comunicação via rede interna

 **Usuários não-root**
- Todos os containers rodam como `houdinis` user
- Não há privilégios root

 **Volumes read-only**
- Código em modo read-only
- Apenas resultados são read-write

### Portas Expostas

**APENAS uma porta exposta ao host:**

| Porta | Serviço | Acesso |
|-------|---------|--------|
| 8080 | Web UI | http://localhost:8080 |

**Todas as outras portas são internas:**

| Porta | Serviço | Rede |
|-------|---------|------|
| 11434 | Ollama | Interna |
| 8000 | ChromaDB | Interna |
| 6379 | Redis | Interna |
| 22 | Target SSH | Interna |

### Credenciais Padrão

** TROCAR IMEDIATAMENTE:**

```bash
# Web UI
Username: admin
Password: houdinis123

# Redis
Password: houdinis_redis_pass

# ChromaDB
Token: houdinis_chroma_token
```

**Como trocar:**

1. Edite `.env` file:
```bash
nano .env

SECRET_KEY=seu-secret-key-aqui
REDIS_PASSWORD=sua-senha-redis
CHROMA_TOKEN=seu-token-chroma
```

2. Rebuild:
```bash
docker compose -f docker/docker-compose-full.yml down
docker compose -f docker/docker-compose-full.yml up -d
```

---

##  FAQ

### Por que 100% Docker?

**Vantagens:**
1.  **Zero poluição** do laptop
2.  **Isolamento** total
3.  **Reprodutível** em qualquer máquina
4.  **Fácil de limpar** (docker down)
5.  **Seguro** (sem privilégios root)
6.  **Portável** (deploy em qualquer servidor)

### Posso rodar sem GPU?

**Sim!** GPU é opcional:

- **Com GPU:** Simulações 10-50x mais rápidas
- **Sem GPU:** Funciona em CPU (mais lento)

### Quanto espaço em disco preciso?

| Perfil | Disk Space |
|--------|------------|
| LITE | 10GB |
| AI POWERED | 20GB |
| FULL STACK | 30GB |
| ENTERPRISE | 100GB |

### Posso acessar de outro computador?

**Sim!** Mude a porta binding:

```yaml
# docker-compose-full.yml
services:
  webui:
    ports:
      - "0.0.0.0:8080:8080"  # Aceita de qualquer IP
```

Então acesse: `http://IP_DO_SERVIDOR:8080`

### Como backup dos resultados?

```bash
# Backup volume
docker run --rm \
  -v houdinis_results:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/results-backup.tar.gz /data

# Restore
docker run --rm \
  -v houdinis_results:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/results-backup.tar.gz -C /
```

### Funciona no Windows/Mac?

**Sim!** Docker funciona em:
-  Linux (nativo, melhor performance)
-  Windows 10/11 (via WSL2)
-  macOS (via Docker Desktop)

** GPU support:**
- Linux: Full support
- Windows: Via WSL2 + NVIDIA drivers
- macOS: CPU only (sem CUDA)

---

##  Documentação Adicional

- **[User Guide](USER_GUIDE.md)** - Como usar a Web UI
- **[API Reference](API_REFERENCE.md)** - API endpoints
- **[Exploits Guide](EXPLOITS.md)** - Lista de exploits
- **[Mistral AI Guide](MISTRAL_LOCAL_GUIDE.md)** - AI assistant

---

##  Suporte

**Issues:** https://github.com/maurorisonho/Houdinis/issues  
**Email:** mauro.risonho@gmail.com  
**Docs:** `docs/` directory

---

** Agora você tem um framework de quantum crypto 100% containerizado!**

**Comece agora:**
```bash
./deploy-docker.sh
```
