#  Docker Image Management - Houdinis Framework

##  Current Images Status

```bash
IMAGEM                  TAMANHO    STATUS

houdinis-mistral        26.4GB      ACTIVE (Ollama + Mistral 7B)
houdinis-core           20.7GB      ACTIVE  
houdinis-webui          720MB       ACTIVE
nvidia/cuda (base)      346MB       BASE IMAGE

TOTAL                   ~48GB

 Nota: Imagens antigas (docker_houdinis, docker-houdinis) foram 
    removidas - arquitetura migrada para modelo modular (core + mistral + webui)
```

---

##  **Migração Arquitetural (Dezembro 2025)**

**Arquitetura Antiga (Removida):**
- `docker_houdinis` (21.5GB) - Monolítico 
- `docker-houdinis` (14.8GB) - Versão anterior 

**Nova Arquitetura Modular (Ativa):**
- `houdinis-mistral` (26.4GB) - AI + Ollama + Mistral 7B 
- `houdinis-core` (20.7GB) - Framework core + exploits 
- `houdinis-webui` (720MB) - Interface web 

**Vantagens:**
-  Componentes independentes (escala melhor)
-  Updates parciais (não precisa rebuildar tudo)
-  Menor consumo de recursos (liga só o que precisa)

---

##  **SIM! As imagens são PERMANENTES**

###  **Como Docker funciona:**

1. **Imagens ficam salvas no disco**
   - Local: `/var/lib/docker/`
   - Persistem após desligar o container
   - Apenas `docker rmi` remove

2. **Containers vs Imagens**
   ```bash
   Container = Instância TEMPORÁRIA da imagem
   Imagem = TEMPLATE permanente no disco
   ```

3. **Volumes também são permanentes**
   ```bash
   ollama_models          # Mistral 7B model (4.4GB)
   vectorstore_local      # ChromaDB data
   ```

---

##  **Gerenciamento de Containers**

### **Parar containers (IMAGEM permanece)**
```bash
# Parar Mistral
docker stop houdinis_mistral

# Parar todos
docker compose -f docker/docker-compose-lite.yml down

#  IMAGEM continua no disco!
```

### **Reiniciar depois (RÁPIDO - sem rebuild)**
```bash
# Iniciar Mistral
docker start houdinis_mistral

# Ou com compose
docker compose -f docker/docker-compose-lite.yml up -d mistral

#  Inicia em segundos (não precisa rebuild!)
```

### **Status dos containers**
```bash
# Ver containers rodando
docker ps

# Ver TODOS (incluindo parados)
docker ps -a

# Ver imagens salvas
docker images
```

---

##  **Backup e Portabilidade**

### **Exportar imagem para arquivo**
```bash
# Exportar Mistral (26.4GB → arquivo .tar)
docker save houdinis-mistral:latest -o mistral-backup.tar

# Compactar (reduz ~50%)
docker save houdinis-mistral:latest | gzip > mistral-backup.tar.gz
```

### **Importar em outra máquina**
```bash
# Carregar imagem do arquivo
docker load -i mistral-backup.tar

# Verificar
docker images | grep mistral
```

### **Push para Docker Hub (opcional)**
```bash
# Login
docker login

# Tag
docker tag houdinis-mistral:latest maurorisonho/houdinis-mistral:latest

# Push
docker push maurorisonho/houdinis-mistral:latest

# Pull em qualquer lugar
docker pull maurorisonho/houdinis-mistral:latest
```

---

##  **Limpeza de Espaço (quando necessário)**

### **Remover containers parados**
```bash
docker container prune
```

### **Remover imagens não utilizadas**
```bash
# Imagens "dangling" (sem tag)
docker image prune

# TODAS imagens não utilizadas
docker image prune -a
```

### **Remover imagem específica**
```bash
docker rmi houdinis-mistral:latest
```

### **Limpeza completa (CUIDADO!)**
```bash
# Remove TUDO não usado
docker system prune -a --volumes

#  Isso remove:
# - Containers parados
# - Imagens não utilizadas
# - Volumes não utilizados
# - Cache de build
```

---

##  **Monitoramento de Espaço**

### **Ver uso total**
```bash
docker system df
```

### **Detalhado por imagem**
```bash
docker system df -v
```

### **Espaço em disco**
```bash
df -h /var/lib/docker
```

---

##  **Workflow Recomendado**

### **Dia-a-dia (desenvolvimento)**
```bash
# Manhã: Iniciar
docker compose -f docker/docker-compose-lite.yml up -d

# Trabalhar...

# Noite: Parar (libera RAM)
docker compose -f docker/docker-compose-lite.yml stop

#  Imagens permanecem no disco
```

### **Fim de semana/férias**
```bash
# Parar e remover containers
docker compose -f docker/docker-compose-lite.yml down

# Imagens ainda no disco
docker images | grep houdinis

# Reiniciar quando voltar (rápido!)
docker compose -f docker/docker-compose-lite.yml up -d
```

### **Backup antes de atualização**
```bash
# 1. Backup imagem atual
docker save houdinis-mistral:latest | gzip > backup-$(date +%Y%m%d).tar.gz

# 2. Rebuild nova versão
python3 build-mistral-detailed.py

# 3. Se der problema, restaurar
docker load -i backup-20251216.tar.gz
```

---

##  **Dicas de Otimização**

### **1. Multi-stage builds** (já implementado)
```dockerfile
# Reduz tamanho final
FROM nvidia/cuda:12.4.1-devel AS builder
# ... compilação ...
FROM nvidia/cuda:12.4.1-base
COPY --from=builder /artifacts /
```

### **2. Layer caching**
```bash
# Rebuild aproveita layers anteriores
# Só rebuilda o que mudou
```

### **3. .dockerignore**
```bash
# Exclui arquivos desnecessários do build
__pycache__/
*.pyc
.git/
.venv/
```

---

##  **Resumo: O que é permanente?**

| Item | Permanente? | Localização | Como remover |
|------|-------------|-------------|--------------|
| **Imagem Docker** |  SIM | /var/lib/docker/ | `docker rmi` |
| **Container parado** |  SIM | /var/lib/docker/ | `docker rm` |
| **Volume** |  SIM | /var/lib/docker/volumes/ | `docker volume rm` |
| **Container rodando** | ⏸ TEMPORÁRIO | RAM + disco | `docker stop` |
| **Build cache** |  SIM | /var/lib/docker/ | `docker builder prune` |

---

##  **Quick Reference**

```bash
# Ver imagens salvas
docker images

# Ver espaço usado
docker system df

# Parar containers (imagem fica)
docker compose -f docker/docker-compose-lite.yml stop

# Reiniciar (rápido!)
docker compose -f docker/docker-compose-lite.yml start

# Backup imagem
docker save houdinis-mistral | gzip > backup.tar.gz

# Restaurar
docker load < backup.tar.gz

# Limpeza segura
docker container prune
docker image prune

# Limpeza agressiva (CUIDADO!)
docker system prune -a
```

---

##  **Conclusão**

**Suas imagens Docker (26.4GB Mistral + 20.7GB Core + etc) estão SALVAS no disco permanentemente!**

-  Pode parar containers à vontade
-  Reinicia em segundos (sem rebuild)
-  Sobrevive a reinicializações do sistema
-  Só é removida com `docker rmi` explícito

**Não precisa refazer o build de 93 minutos!** 
