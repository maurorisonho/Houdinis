# Houdinis - Guia de Infraestrutura e Deploy

##  Visão Geral

Este documento explica a diferença entre o **ambiente de desenvolvimento local** e a **infraestrutura de produção na nuvem**, além de como configurar o pipeline CI/CD.

---

##  Ambiente Local (Desenvolvimento)

### O que funciona localmente:
-  Execução de todos os exploits quânticos
-  Testes unitários e de integração
-  Docker containers locais
-  Simuladores quânticos (Qiskit, Cirq)
-  Benchmarking e profiling
-  Notebooks Jupyter

### Requisitos locais:
```bash
# Hardware mínimo
- CPU: 4+ cores
- RAM: 8GB+ (16GB recomendado para simulações grandes)
- Disco: 10GB+ livre

# Software
- Python 3.11+
- Docker (opcional)
- Git
```

---

##  Infraestrutura na Nuvem (Produção)

###  O que NÃO existe ainda:

1. **Computadores Quânticos Reais na Nuvem**
   -  Sem acesso configurado ao IBM Quantum Experience
   -  Sem acesso ao Azure Quantum
   -  Sem acesso ao AWS Braket
   -  Sem acesso ao Google Quantum AI

2. **Infraestrutura Kubernetes**
   -  Sem cluster EKS (AWS)
   -  Sem cluster AKS (Azure)
   -  Sem cluster GKE (Google Cloud)

3. **Serviços de Deploy Automático**
   -  Sem ambiente staging/production configurado
   -  Sem load balancers configurados
   -  Sem auto-scaling configurado

4. **Publicação de Pacotes**
   -  Sem conta PyPI configurada
   -  Token PYPI_API_TOKEN não configurado

---

##  CI/CD Atual (GitHub Actions)

### O que está configurado e **FUNCIONA**:

####  1. Lint & Code Quality
```yaml
Jobs executados automaticamente:
- Black formatter check
- isort import checker
- flake8 linting
- Pyright type checking
```
**Requer:** Nada além do GitHub

####  2. Security Scanning
```yaml
Jobs executados automaticamente:
- bandit (security issues)
- safety (vulnerable dependencies)
- Trivy (Docker vulnerabilities)
```
**Requer:** Nada além do GitHub

####  3. Unit Tests
```yaml
Jobs executados automaticamente:
- pytest em Python 3.11, 3.12, 3.13
- Testes em Ubuntu, macOS, Windows
- Coverage report com Codecov
```
**Requer:** Nada além do GitHub (Codecov é gratuito para repos públicos)

####  4. Integration Tests
```yaml
Jobs executados automaticamente:
- Testes de integração end-to-end
- Timeout de 5 minutos
```
**Requer:** Nada além do GitHub

####  5. Docker Build
```yaml
Jobs executados automaticamente:
- Build de imagens Docker
- Teste de container
```
**Requer:** Nada além do GitHub

####  6. Package Build
```yaml
Jobs executados automaticamente:
- Build do pacote Python
- Validação com twine
- Upload de artefatos
```
**Requer:** Nada além do GitHub

---

###  O que NÃO vai funcionar (requer configuração):

####  7. Publish to PyPI
```yaml
# Este job SÓ executa se:
if: github.event_name == 'push' && 
    startsWith(github.ref, 'refs/tags/v') && 
    secrets.PYPI_API_TOKEN != ''
```

**Requer:**
1. Conta no PyPI (https://pypi.org)
2. Criar API Token no PyPI
3. Adicionar secret `PYPI_API_TOKEN` no GitHub:
   - Ir em: Repositório → Settings → Secrets and variables → Actions
   - New repository secret
   - Name: `PYPI_API_TOKEN`
   - Value: `pypi-...` (seu token)

**Como obter o token:**
```bash
1. Criar conta em https://pypi.org
2. Verificar email
3. Account Settings → API tokens → Add API token
4. Scope: "Entire account" ou específico para "houdinis"
5. Copiar token (começa com pypi-...)
```

---

##  Cenários de Deploy

### Cenário 1: Apenas Desenvolvimento (ATUAL)
```
 GitHub Actions CI/CD
    Lint & Security 
    Tests 
    Docker Build 
    Package Build 

 Deploy to PyPI - DESABILITADO (sem token)
 Deploy to Cloud - NÃO CONFIGURADO
 Quantum Hardware - LOCAL SIMULATORS ONLY
```

**O que fazer:**
- Usar apenas para desenvolvimento local
- CI/CD valida código automaticamente em PRs
- Não tenta fazer deploy (não vai falhar)

---

### Cenário 2: Deploy no PyPI (SIMPLES)

**Passo 1 - Configurar PyPI:**
```bash
# 1. Criar conta no PyPI
https://pypi.org/account/register/

# 2. Criar API Token
Account Settings → API tokens → Add API token

# 3. Adicionar secret no GitHub
Repositório → Settings → Secrets → Actions
Nome: PYPI_API_TOKEN
Valor: pypi-AgEIcHlwaS5vcmcC...
```

**Passo 2 - Publicar release:**
```bash
# Criar tag de versão
git tag v1.0.0
git push origin v1.0.0

# GitHub Actions automaticamente:
# 1. Executa todos os testes 
# 2. Build do pacote 
# 3. Publica no PyPI  (agora funciona)
```

**Passo 3 - Instalar de qualquer lugar:**
```bash
pip install houdinis
```

---

### Cenário 3: Deploy em Cloud Kubernetes (COMPLEXO)

** Requer infraestrutura paga na nuvem**

#### Opção A: AWS EKS
```bash
# Custos estimados: $150-300/mês
# - EKS cluster: ~$73/mês
# - EC2 nodes: ~$100/mês
# - Load balancer: ~$20/mês
# - Storage: ~$10/mês

# 1. Criar cluster EKS
eksctl create cluster --name houdinis-cluster --region us-east-1

# 2. Configurar kubectl
aws eks update-kubeconfig --name houdinis-cluster

# 3. Aplicar manifests
kubectl apply -f k8s/

# 4. Configurar secrets no GitHub
# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY
# AWS_REGION
# KUBE_CONFIG_DATA
```

#### Opção B: Azure AKS
```bash
# Custos estimados: $120-250/mês

# 1. Criar cluster AKS
az aks create --resource-group houdinis-rg --name houdinis-cluster

# 2. Configurar kubectl
az aks get-credentials --resource-group houdinis-rg --name houdinis-cluster

# 3. Aplicar manifests
kubectl apply -f k8s/
```

#### Opção C: Google Cloud GKE
```bash
# Custos estimados: $100-200/mês

# 1. Criar cluster GKE
gcloud container clusters create houdinis-cluster --zone us-central1-a

# 2. Configurar kubectl
gcloud container clusters get-credentials houdinis-cluster

# 3. Aplicar manifests
kubectl apply -f k8s/
```

---

### Cenário 4: Acesso a Quantum Hardware Real (MUITO COMPLEXO)

#### IBM Quantum Experience
```bash
# Custos: Grátis (tier básico) até $100K+/ano (enterprise)

# 1. Criar conta
https://quantum-computing.ibm.com/

# 2. Gerar API Token
Account → API Token

# 3. Adicionar ao GitHub Secrets
# IBM_QUANTUM_TOKEN

# 4. Configurar backend no código
from qiskit_ibm_runtime import QiskitRuntimeService
service = QiskitRuntimeService(channel="ibm_quantum", token="YOUR_TOKEN")
backend = service.backend("ibmq_manila")  # Computador quântico real
```

#### AWS Braket
```bash
# Custos: $0.30 por tarefa + $0.00035 por shot

# 1. Habilitar AWS Braket
AWS Console → Braket → Enable

# 2. Configurar credenciais
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY

# 3. Usar backend
from braket.aws import AwsDevice
device = AwsDevice("arn:aws:braket:::device/quantum-simulator/amazon/sv1")
```

---

##  Resumo: O que funciona HOJE

###  Funciona sem configuração adicional:
```
1.  Desenvolvimento local completo
2.  Testes automatizados (GitHub Actions)
3.  Linting e security scans
4.  Docker builds
5.  Coverage reports
6.  Simuladores quânticos locais
```

###  Funciona com configuração simples (grátis):
```
7.  Publish to PyPI
   Requer: Token do PyPI (5 minutos para configurar)
   Custo: GRÁTIS
```

###  NÃO funciona (requer infraestrutura paga):
```
8.  Deploy em Kubernetes Cloud
   Requer: Cluster K8s na AWS/Azure/GCP
   Custo: $100-300/mês

9.  Quantum Hardware Real
   Requer: Conta IBM Quantum/AWS Braket
   Custo: $0 (free tier) até $100K+/ano
```

---

##  Recomendações

### Para Desenvolvimento (AGORA):
```bash
 Usar ambiente local
 CI/CD já funciona (testes automáticos)
 Docker local funciona
 Simuladores quânticos funcionam
```

### Para Publicação Simples (5 minutos):
```bash
1. Criar conta PyPI
2. Adicionar PYPI_API_TOKEN ao GitHub
3. Criar tag: git tag v1.0.0 && git push origin v1.0.0
4. Pronto! Pacote publicado automaticamente
```

### Para Produção Enterprise (semanas + $$$):
```bash
1. Escolher cloud provider (AWS/Azure/GCP)
2. Criar cluster Kubernetes
3. Configurar secrets no GitHub
4. Configurar acesso a quantum hardware
5. Monitoramento e logging
6. Custos: $500-2000/mês
```

---

##  Secrets Necessários no GitHub

### Mínimo para funcionar (ATUAL):
```
Nenhum! Tudo funciona sem secrets.
```

### Para PyPI (Opcional):
```yaml
PYPI_API_TOKEN: Token do PyPI (pypi-...)
```

### Para Cloud Deploy (Avançado):
```yaml
# AWS
AWS_ACCESS_KEY_ID: Chave de acesso AWS
AWS_SECRET_ACCESS_KEY: Chave secreta AWS
AWS_REGION: us-east-1

# Azure
AZURE_CREDENTIALS: JSON com credenciais
AZURE_SUBSCRIPTION_ID: ID da assinatura

# Google Cloud
GCP_PROJECT_ID: ID do projeto
GCP_SA_KEY: Service account JSON

# Quantum Hardware
IBM_QUANTUM_TOKEN: Token do IBM Quantum
AWS_BRAKET_ROLE: ARN do role do Braket
```

---

##  Conclusão

**Status Atual:**
-  CI/CD funciona 100% para desenvolvimento
-  Nenhuma configuração adicional necessária
-  Não há dependência de infraestrutura cloud
-  Deploy no PyPI requer apenas 1 secret (opcional)
-  Deploy em cloud requer infraestrutura paga (futuro)

**Próximos Passos Recomendados:**
1. Continuar usando ambiente local (funciona perfeitamente)
2. CI/CD valida código automaticamente (já funciona)
3. Quando pronto para publicar: configurar PyPI (5 minutos)
4. Deploy em cloud é OPCIONAL e caro (apenas se necessário)

**Custos:**
- Desenvolvimento: **$0/mês** 
- PyPI publishing: **$0/mês** 
- Cloud deploy: **$100-300/mês**  (não configurado)
- Quantum hardware: **$0-100K+/ano**  (não configurado)
