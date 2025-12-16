# Houdinis - Infrastructure and Deployment Guide

##  Overview

Este documento explica a diferença entre o **ambiente de desenvolvimento local** e a **infraestrutura de produção na nuvem**, além de como configurar o pipeline CI/CD.

---

##  Local Environment (Development)

### What works locally:
-  Execution of all quantum exploits
-  Testes unitários e de integração
-  Docker containers locais
-  Simuladores quânticos (Qiskit, Cirq)
-  Benchmarking e profiling
-  Notebooks Jupyter

### Local requirements:
```bash
# Minimum hardware
- CPU: 4+ cores
- RAM: 8GB+ (16GB recomendado para simulações grandes)
- Disco: 10GB+ livre

# Software
- Python 3.11+
- Docker (opcional)
- Git
```

---

##  Cloud Infrastructure (Production)

###  What does NOT exist yet:

1. **Real Quantum Computers in the Cloud**
   -  No configured access ao IBM Quantum Experience
   -  Sem acesso ao Azure Quantum
   -  Sem acesso ao AWS Braket
   -  Sem acesso ao Google Quantum AI

2. **Kubernetes Infrastructure**
   -  No cluster EKS (AWS)
   -  No cluster AKS (Azure)
   -  No cluster GKE (Google Cloud)

3. **Automatic Deploy Services**
   -  No environment staging/production configurado
   -  No configured load balancers
   -  No configured auto-scaling

4. **Package Publishing**
   -  No configured PyPI account
   -  Token PYPI_API_TOKEN not configured

---

##  Current CI/CD (GitHub Actions)

### What is configured and **WORKS**:

####  1. Lint & Code Quality
```yaml
Jobs executed automatically:
- Black formatter check
- isort import checker
- flake8 linting
- Pyright type checking
```
**Requires:** Nothing besides GitHub

####  2. Security Scanning
```yaml
Jobs executed automatically:
- bandit (security issues)
- safety (vulnerable dependencies)
- Trivy (Docker vulnerabilities)
```
**Requires:** Nothing besides GitHub

####  3. Unit Tests
```yaml
Jobs executed automatically:
- pytest em Python 3.11, 3.12, 3.13
- Testes em Ubuntu, macOS, Windows
- Coverage report com Codecov
```
**Requires:** Nothing besides GitHub (Codecov é gratuito para repos públicos)

####  4. Integration Tests
```yaml
Jobs executed automatically:
- Testes de integração end-to-end
- Timeout de 5 minutos
```
**Requires:** Nothing besides GitHub

####  5. Docker Build
```yaml
Jobs executed automatically:
- Build de imagens Docker
- Teste de container
```
**Requires:** Nothing besides GitHub

####  6. Package Build
```yaml
Jobs executed automatically:
- Build do pacote Python
- Validação com twine
- Upload de artefatos
```
**Requires:** Nothing besides GitHub

---

###  What will NOT work (requires configuration):

####  7. Publish to PyPI
```yaml
# This job ONLY executes if:
if: github.event_name == 'push' && 
    startsWith(github.ref, 'refs/tags/v') && 
    secrets.PYPI_API_TOKEN != ''
```

**Requires:**
1. PyPI Account (https://pypi.org)
2. Criar API Token no PyPI
3. Add secret `PYPI_API_TOKEN` no GitHub:
   - Ir em: Repositório → Settings → Secrets and variables → Actions
   - New repository secret
   - Name: `PYPI_API_TOKEN`
   - Value: `pypi-...` (seu token)

**How to get the token:**
```bash
1. Create account at https://pypi.org
2. Verify email
3. Account Settings → API tokens → Add API token
4. Scope: "Entire account" ou específico para "houdinis"
5. Copy token (starts with pypi-...)
```

---

##  Deployment Scenarios

### Scenario 1: Development Only (CURRENT)
```
 GitHub Actions CI/CD
    Lint & Security 
    Tests 
    Docker Build 
    Package Build 

 Deploy to PyPI - DISABLED (no token)
 Deploy to Cloud - NOT CONFIGURED
 Quantum Hardware - LOCAL SIMULATORS ONLY
```

**What to do:**
- Use only for local development
- CI/CD validates code automatically in PRs
- Does not attempt deploy (will not fail)

---

### Scenario 2: Deploy no PyPI (SIMPLES)

**Passo 1 - Configure PyPI:**
```bash
# 1. Criar conta no PyPI
https://pypi.org/account/register/

# 2. Criar API Token
Account Settings → API tokens → Add API token

# 3. Add secret no GitHub
Repositório → Settings → Secrets → Actions
Nome: PYPI_API_TOKEN
Valor: pypi-AgEIcHlwaS5vcmcC...
```

**Passo 2 - Publicar release:**
```bash
# Create version tag
git tag v1.0.0
git push origin v1.0.0

# GitHub Actions automatically:
# 1. Executes all tests 
# 2. Build do pacote 
# 3. Publishes to PyPI  (now works)
```

**Passo 3 - Install from anywhere:**
```bash
pip install houdinis
```

---

### Scenario 3: Deploy em Cloud Kubernetes (COMPLEXO)

** Requires infraestrutura paga na nuvem**

#### Opção A: AWS EKS
```bash
# Estimated costs: $150-300/mês
# - EKS cluster: ~$73/mês
# - EC2 nodes: ~$100/mês
# - Load balancer: ~$20/mês
# - Storage: ~$10/mês

# 1. Create cluster EKS
eksctl create cluster --name houdinis-cluster --region us-east-1

# 2. Configure kubectl
aws eks update-kubeconfig --name houdinis-cluster

# 3. Apply manifests
kubectl apply -f k8s/

# 4. Configure secrets in GitHub
# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY
# AWS_REGION
# KUBE_CONFIG_DATA
```

#### Opção B: Azure AKS
```bash
# Estimated costs: $120-250/mês

# 1. Create cluster AKS
az aks create --resource-group houdinis-rg --name houdinis-cluster

# 2. Configure kubectl
az aks get-credentials --resource-group houdinis-rg --name houdinis-cluster

# 3. Apply manifests
kubectl apply -f k8s/
```

#### Opção C: Google Cloud GKE
```bash
# Estimated costs: $100-200/mês

# 1. Create cluster GKE
gcloud container clusters create houdinis-cluster --zone us-central1-a

# 2. Configure kubectl
gcloud container clusters get-credentials houdinis-cluster

# 3. Apply manifests
kubectl apply -f k8s/
```

---

### Scenario 4: Access to Real Quantum Hardware (VERY COMPLEX)

#### IBM Quantum Experience
```bash
# Costs: Free (basic tier) até $100K+/ano (enterprise)

# 1. Criar conta
https://quantum-computing.ibm.com/

# 2. Generate API Token
Account → API Token

# 3. Add to GitHub Secrets
# IBM_QUANTUM_TOKEN

# 4. Configure backend in code
from qiskit_ibm_runtime import QiskitRuntimeService
service = QiskitRuntimeService(channel="ibm_quantum", token="YOUR_TOKEN")
backend = service.backend("ibmq_manila")  # Real quantum computer
```

#### AWS Braket
```bash
# Costs: $0.30 per task + $0.00035 per shot

# 1. Enable AWS Braket
AWS Console → Braket → Enable

# 2. Configure credentials
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY

# 3. Use backend
from braket.aws import AwsDevice
device = AwsDevice("arn:aws:braket:::device/quantum-simulator/amazon/sv1")
```

---

##  Summary: What works TODAY

###  Works without additional configuration:
```
1.  Complete local development
2.  Automated tests (GitHub Actions)
3.  Linting and security scans
4.  Docker builds
5.  Coverage reports
6.  Local quantum simulators
```

###  Works with simple configuration (free):
```
7.  Publish to PyPI
   Requires: PyPI Token (5 minutes to configure)
   Cost: FREE
```

###  Does NOT work (requires paid infrastructure):
```
8.  Deploy to Kubernetes Cloud
   Requires: K8s Cluster on AWS/Azure/GCP
   Cost: $100-300/mês

9.  Real Quantum Hardware
   Requires: Conta IBM Quantum/AWS Braket
   Cost: $0 (free tier) até $100K+/ano
```

---

##  Recommendations

### For Development (NOW):
```bash
 Use local environment
 CI/CD already works (automatic tests)
 Local Docker works
 Quantum simulators work
```

### For Simple Publishing (5 minutos):
```bash
1. Criar conta PyPI
2. Adicionar PYPI_API_TOKEN ao GitHub
3. Criar tag: git tag v1.0.0 && git push origin v1.0.0
4. Pronto! Pacote publicado automatically
```

### For Enterprise Production (weeks + $$$):
```bash
1. Choose cloud provider (AWS/Azure/GCP)
2. Create cluster Kubernetes
3. Configure secrets in GitHub
4. Configurar acesso a quantum hardware
5. Monitoramento e logging
6. Costs: $500-2000/mês
```

---

##  Required Secrets in GitHub

### Minimum to work (CURRENT):
```
Nenhum! Everything works without secrets.
```

### For PyPI (Optional):
```yaml
PYPI_API_TOKEN: PyPI Token (pypi-...)
```

### For Cloud Deploy (Advanced):
```yaml
# AWS
AWS_ACCESS_KEY_ID: Access key AWS
AWS_SECRET_ACCESS_KEY: Secret key AWS
AWS_REGION: us-east-1

# Azure
AZURE_CREDENTIALS: JSON with credentials
AZURE_SUBSCRIPTION_ID: Subscription ID

# Google Cloud
GCP_PROJECT_ID: Project ID
GCP_SA_KEY: Service account JSON

# Quantum Hardware
IBM_QUANTUM_TOKEN: Token do IBM Quantum
AWS_BRAKET_ROLE: ARN of role of Braket
```

---

##  Conclusion

**Current Status:**
-  CI/CD works 100% for development
-  No additional configuration needed
-  No cloud infrastructure dependency
-  Deploy no PyPI requires only 1 secret (optional)
-  Deploy em cloud requires paid infrastructure (future)

**Recommended Next Steps:**
1. Continue using local environment (works perfectly)
2. CI/CD valida código automatically (já funciona)
3. When ready to publish: configure PyPI (5 minutos)
4. Cloud deploy is OPTIONAL and expensive (only if needed)

**Costs:**
- Desenvolvimento: **$0/mês** 
- PyPI publishing: **$0/mês** 
- Cloud deploy: **$100-300/mês**  (not configured)
- Quantum hardware: **$0-100K+/ano**  (not configured)
