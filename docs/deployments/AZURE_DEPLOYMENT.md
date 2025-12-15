# Azure Deployment Guide

Complete guide for deploying Houdinis Framework on Microsoft Azure.

## Table of Contents
- [Architecture Overview](#architecture-overview)
- [Prerequisites](#prerequisites)
- [Deployment Options](#deployment-options)
  - [Azure Container Instances (ACI)](#aci-deployment)
  - [Azure Kubernetes Service (AKS)](#aks-deployment)
  - [Azure Container Apps](#container-apps-deployment)
  - [Azure VM with Docker](#vm-deployment)
- [Configuration](#configuration)
- [Monitoring](#monitoring)
- [Scaling](#scaling)
- [Security](#security)
- [Troubleshooting](#troubleshooting)
- [Cost Optimization](#cost-optimization)

---

## Architecture Overview

```

                      Azure Cloud                         
                                                           
               
     Azure       Application   WAF    
      DNS               Gateway                   
               
                                                         
                                                         
                                       
                      AKS/ACI                           
                      Cluster                           
                                       
                   /       |       \                      
                      
         Container1  Contain2  Container3         
         Houdinis                                 
                      
                                                           
       
    Blob         Azure         Key Vault         
   Storage      Monitor       Secrets/Certs      
       

```

---

## Prerequisites

### Azure CLI
```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login
az login

# Set subscription
az account set --subscription "YOUR_SUBSCRIPTION_ID"

# Verify
az account show
```

### Required Extensions
```bash
# Install AKS preview extension
az extension add --name aks-preview
az extension update --name aks-preview

# Install container instances extension
az extension add --name container-app
```

### Resource Group
```bash
# Create resource group
az group create \
  --name houdinis-rg \
  --location eastus

# Set as default
az configure --defaults group=houdinis-rg location=eastus
```

---

## Deployment Options

### ACI Deployment

Azure Container Instances (ACI) provides the fastest and simplest way to run containers.

#### 1. Quick Start
```bash
# Deploy container
az container create \
  --name houdinis \
  --image maurorisonho/houdinis:latest \
  --resource-group houdinis-rg \
  --location eastus \
  --cpu 2 \
  --memory 4 \
  --ports 8000 \
  --dns-name-label houdinis-app \
  --environment-variables \
    PYTHONUNBUFFERED=1 \
    LOG_LEVEL=INFO \
  --secure-environment-variables \
    IBM_QUANTUM_TOKEN=your_token_here \
  --restart-policy OnFailure

# Get public IP
az container show \
  --name houdinis \
  --query ipAddress.fqdn \
  --output tsv

# View logs
az container logs --name houdinis --follow
```

#### 2. Deploy with YAML
**aci-deployment.yaml:**
```yaml
apiVersion: 2021-09-01
location: eastus
name: houdinis-container-group
properties:
  containers:
  - name: houdinis
    properties:
      image: maurorisonho/houdinis:latest
      resources:
        requests:
          cpu: 2
          memoryInGb: 4
      ports:
      - port: 8000
        protocol: TCP
      environmentVariables:
      - name: PYTHONUNBUFFERED
        value: "1"
      - name: LOG_LEVEL
        value: INFO
      - name: IBM_QUANTUM_TOKEN
        secureValue: YOUR_TOKEN_FROM_KEY_VAULT
      volumeMounts:
      - name: output
        mountPath: /app/output
      livenessProbe:
        exec:
          command:
          - python
          - -c
          - "import sys; sys.exit(0)"
        initialDelaySeconds: 30
        periodSeconds: 10
  osType: Linux
  restartPolicy: OnFailure
  ipAddress:
    type: Public
    ports:
    - protocol: TCP
      port: 8000
    dnsNameLabel: houdinis-app
  volumes:
  - name: output
    azureFile:
      shareName: houdinis-output
      storageAccountName: houdinisstorage
      storageAccountKey: YOUR_STORAGE_KEY
tags:
  project: houdinis
  environment: production
type: Microsoft.ContainerInstance/containerGroups
```

Deploy:
```bash
az container create \
  --resource-group houdinis-rg \
  --file aci-deployment.yaml
```

#### 3. Setup Azure Files for Persistence
```bash
# Create storage account
az storage account create \
  --name houdinisstorage \
  --sku Standard_LRS

# Get connection string
STORAGE_KEY=$(az storage account keys list \
  --account-name houdinisstorage \
  --query '[0].value' \
  --output tsv)

# Create file share
az storage share create \
  --name houdinis-output \
  --account-name houdinisstorage \
  --account-key $STORAGE_KEY

# Mount in container (see YAML above)
```

---

### AKS Deployment

Azure Kubernetes Service (AKS) for production workloads.

#### 1. Create AKS Cluster
```bash
# Create cluster (10-15 minutes)
az aks create \
  --name houdinis-aks \
  --node-count 3 \
  --node-vm-size Standard_D2s_v3 \
  --enable-managed-identity \
  --enable-addons monitoring \
  --enable-cluster-autoscaler \
  --min-count 1 \
  --max-count 5 \
  --generate-ssh-keys

# Get credentials
az aks get-credentials --name houdinis-aks

# Verify connection
kubectl get nodes
```

#### 2. Create Azure Container Registry (ACR)
```bash
# Create registry
az acr create \
  --name houdinisacr \
  --sku Basic

# Attach to AKS
az aks update \
  --name houdinis-aks \
  --attach-acr houdinisacr

# Login to ACR
az acr login --name houdinisacr

# Import image from Docker Hub
az acr import \
  --name houdinisacr \
  --source docker.io/maurorisonho/houdinis:latest \
  --image houdinis:latest
```

#### 3. Deploy to AKS
**k8s/deployment-azure.yaml:**
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: houdinis
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: houdinis-config
  namespace: houdinis
data:
  PYTHONUNBUFFERED: "1"
  LOG_LEVEL: "INFO"
  AZURE_REGION: "eastus"
---
apiVersion: v1
kind: Secret
metadata:
  name: houdinis-secrets
  namespace: houdinis
type: Opaque
stringData:
  IBM_QUANTUM_TOKEN: "your_token_here"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: houdinis
  namespace: houdinis
  labels:
    app: houdinis
    version: v1
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: houdinis
  template:
    metadata:
      labels:
        app: houdinis
        version: v1
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "9090"
    spec:
      serviceAccountName: houdinis
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault
      containers:
      - name: houdinis
        image: houdinisacr.azurecr.io/houdinis:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 8000
          name: http
          protocol: TCP
        env:
        - name: AZURE_STORAGE_ACCOUNT
          value: "houdinisstorage"
        - name: AZURE_STORAGE_KEY
          valueFrom:
            secretKeyRef:
              name: azure-storage-secret
              key: storage-key
        envFrom:
        - configMapRef:
            name: houdinis-config
        - secretRef:
            name: houdinis-secrets
        resources:
          requests:
            cpu: 500m
            memory: 1Gi
          limits:
            cpu: 2000m
            memory: 4Gi
        livenessProbe:
          exec:
            command:
            - python
            - -c
            - "import sys; sys.exit(0)"
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          exec:
            command:
            - python
            - -c
            - "from core import cli; sys.exit(0)"
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
        volumeMounts:
        - name: output
          mountPath: /app/output
        - name: azure-storage
          mountPath: /mnt/azure
      volumes:
      - name: output
        persistentVolumeClaim:
          claimName: houdinis-pvc
      - name: azure-storage
        azureFile:
          secretName: azure-storage-secret
          shareName: houdinis-output
          readOnly: false
---
apiVersion: v1
kind: Service
metadata:
  name: houdinis
  namespace: houdinis
  annotations:
    service.beta.kubernetes.io/azure-load-balancer-internal: "false"
spec:
  type: LoadBalancer
  selector:
    app: houdinis
  ports:
  - port: 80
    targetPort: 8000
    protocol: TCP
    name: http
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: houdinis-hpa
  namespace: houdinis
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: houdinis
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 15
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
      - type: Pods
        value: 2
        periodSeconds: 15
      selectPolicy: Max
```

Deploy:
```bash
# Apply manifests
kubectl apply -f k8s/deployment-azure.yaml

# Verify deployment
kubectl get all -n houdinis

# Get external IP
kubectl get svc -n houdinis

# View logs
kubectl logs -n houdinis -l app=houdinis --tail=100 -f
```

#### 4. Setup Ingress with Application Gateway
```bash
# Enable Application Gateway Ingress Controller
az aks enable-addons \
  --name houdinis-aks \
  --addons ingress-appgw \
  --appgw-name houdinis-appgw \
  --appgw-subnet-cidr "10.2.0.0/16"

# Create ingress
kubectl apply -f k8s/ingress-azure.yaml
```

**k8s/ingress-azure.yaml:**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: houdinis-ingress
  namespace: houdinis
  annotations:
    kubernetes.io/ingress.class: azure/application-gateway
    appgw.ingress.kubernetes.io/ssl-redirect: "true"
    appgw.ingress.kubernetes.io/connection-draining: "true"
    appgw.ingress.kubernetes.io/connection-draining-timeout: "30"
spec:
  rules:
  - host: houdinis.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: houdinis
            port:
              number: 80
  tls:
  - hosts:
    - houdinis.example.com
    secretName: houdinis-tls
```

---

### Container Apps Deployment

Azure Container Apps - serverless containers with auto-scaling.

```bash
# Create Container App environment
az containerapp env create \
  --name houdinis-env \
  --resource-group houdinis-rg \
  --location eastus

# Create Container App
az containerapp create \
  --name houdinis-app \
  --resource-group houdinis-rg \
  --environment houdinis-env \
  --image maurorisonho/houdinis:latest \
  --target-port 8000 \
  --ingress external \
  --cpu 1.0 \
  --memory 2.0Gi \
  --min-replicas 1 \
  --max-replicas 10 \
  --env-vars \
    PYTHONUNBUFFERED=1 \
    LOG_LEVEL=INFO \
  --secrets \
    ibm-token=your_token_here \
  --scale-rule-name http-rule \
  --scale-rule-type http \
  --scale-rule-http-concurrency 100

# Get FQDN
az containerapp show \
  --name houdinis-app \
  --query properties.configuration.ingress.fqdn \
  --output tsv
```

---

### VM Deployment

#### 1. Create VM
```bash
# Create VM
az vm create \
  --name houdinis-vm \
  --image Ubuntu2204 \
  --size Standard_D2s_v3 \
  --admin-username azureuser \
  --generate-ssh-keys \
  --public-ip-sku Standard \
  --custom-data cloud-init.yaml

# Open port 8000
az vm open-port \
  --name houdinis-vm \
  --port 8000 \
  --priority 1001
```

**cloud-init.yaml:**
```yaml
#cloud-config
package_upgrade: true
packages:
  - docker.io
  - docker-compose

runcmd:
  - systemctl start docker
  - systemctl enable docker
  - usermod -aG docker azureuser
  - docker pull maurorisonho/houdinis:latest
  - docker run -d --name houdinis --restart unless-stopped -p 8000:8000 -v /data/houdinis:/app/output maurorisonho/houdinis:latest
  
write_files:
  - path: /etc/systemd/system/houdinis.service
    content: |
      [Unit]
      Description=Houdinis Container
      After=docker.service
      Requires=docker.service
      
      [Service]
      Restart=always
      ExecStart=/usr/bin/docker start -a houdinis
      ExecStop=/usr/bin/docker stop -t 10 houdinis
      
      [Install]
      WantedBy=multi-user.target
```

---

## Configuration

### Key Vault Integration
```bash
# Create Key Vault
az keyvault create \
  --name houdinis-kv \
  --enabled-for-deployment true \
  --enabled-for-template-deployment true

# Store secrets
az keyvault secret set \
  --vault-name houdinis-kv \
  --name ibm-quantum-token \
  --value "YOUR_TOKEN"

# Grant AKS access
az keyvault set-policy \
  --name houdinis-kv \
  --object-id $(az aks show --name houdinis-aks --query identityProfile.kubeletidentity.objectId -o tsv) \
  --secret-permissions get list

# Install CSI driver
az aks enable-addons \
  --name houdinis-aks \
  --addons azure-keyvault-secrets-provider
```

**Use secrets in pods:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: houdinis
spec:
  containers:
  - name: houdinis
    image: houdinisacr.azurecr.io/houdinis:latest
    volumeMounts:
    - name: secrets-store
      mountPath: "/mnt/secrets-store"
      readOnly: true
    env:
    - name: IBM_QUANTUM_TOKEN
      valueFrom:
        secretKeyRef:
          name: keyvault-secrets
          key: ibm-quantum-token
  volumes:
  - name: secrets-store
    csi:
      driver: secrets-store.csi.k8s.io
      readOnly: true
      volumeAttributes:
        secretProviderClass: "azure-keyvault"
```

---

## Monitoring

### Azure Monitor Integration
```bash
# Enable Container Insights
az aks enable-addons \
  --name houdinis-aks \
  --addons monitoring \
  --workspace-resource-id $(az monitor log-analytics workspace create \
    --resource-group houdinis-rg \
    --workspace-name houdinis-workspace \
    --query id -o tsv)

# Create alert rule
az monitor metrics alert create \
  --name houdinis-high-cpu \
  --resource-group houdinis-rg \
  --scopes $(az aks show --name houdinis-aks --query id -o tsv) \
  --condition "avg Percentage CPU > 80" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --action-group houdinis-alerts
```

### Application Insights
```bash
# Create Application Insights
az monitor app-insights component create \
  --app houdinis-insights \
  --location eastus \
  --kind web \
  --application-type web

# Get instrumentation key
INSTRUMENTATION_KEY=$(az monitor app-insights component show \
  --app houdinis-insights \
  --query instrumentationKey -o tsv)

# Add to deployment
kubectl set env deployment/houdinis \
  -n houdinis \
  APPLICATIONINSIGHTS_CONNECTION_STRING="InstrumentationKey=$INSTRUMENTATION_KEY"
```

---

## Scaling

### AKS Node Auto-scaling
```bash
# Enable cluster autoscaler
az aks update \
  --name houdinis-aks \
  --enable-cluster-autoscaler \
  --min-count 1 \
  --max-count 10

# Update autoscaler settings
az aks nodepool update \
  --name nodepool1 \
  --cluster-name houdinis-aks \
  --update-cluster-autoscaler \
  --min-count 2 \
  --max-count 20
```

### Pod Auto-scaling (HPA)
Already configured in deployment YAML above. Verify:
```bash
kubectl get hpa -n houdinis
kubectl describe hpa houdinis-hpa -n houdinis
```

---

## Security

### Network Security Groups
```bash
# Create NSG
az network nsg create --name houdinis-nsg

# Allow HTTPS only
az network nsg rule create \
  --nsg-name houdinis-nsg \
  --name allow-https \
  --priority 100 \
  --destination-port-ranges 443 \
  --access Allow \
  --protocol Tcp

# Deny all other inbound
az network nsg rule create \
  --nsg-name houdinis-nsg \
  --name deny-all-inbound \
  --priority 4096 \
  --access Deny \
  --direction Inbound
```

### Azure Policy
```bash
# Assign policy: Require HTTPS
az policy assignment create \
  --name require-https \
  --policy "/providers/Microsoft.Authorization/policyDefinitions/XXX" \
  --scope $(az group show --name houdinis-rg --query id -o tsv)
```

---

## Troubleshooting

### ACI Issues
```bash
# Check container state
az container show --name houdinis --query instanceView.state

# Stream logs
az container logs --name houdinis --follow

# Restart container
az container restart --name houdinis
```

### AKS Issues
```bash
# Check pod status
kubectl get pods -n houdinis
kubectl describe pod POD_NAME -n houdinis

# View logs
kubectl logs -n houdinis POD_NAME --previous

# Exec into pod
kubectl exec -it -n houdinis POD_NAME -- /bin/bash

# Check events
kubectl get events -n houdinis --sort-by='.lastTimestamp'
```

---

## Cost Optimization

### Use Azure Reservations
- 1-year: ~30% discount
- 3-year: ~60% discount

### Use Spot Instances (AKS)
```bash
# Create spot node pool
az aks nodepool add \
  --cluster-name houdinis-aks \
  --name spotpool \
  --priority Spot \
  --eviction-policy Delete \
  --spot-max-price -1 \
  --node-count 3 \
  --min-count 1 \
  --max-count 10 \
  --enable-cluster-autoscaler
```

### Cost Analysis
```bash
# View cost analysis
az consumption usage list \
  --start-date 2025-01-01 \
  --end-date 2025-01-31 \
  --query "[?contains(instanceName, 'houdinis')]"
```

---

## Complete Deployment Script

**deploy-azure-aks.sh:**
```bash
#!/bin/bash
set -e

RG="houdinis-rg"
LOCATION="eastus"
AKS_NAME="houdinis-aks"
ACR_NAME="houdinisacr"

echo " Deploying Houdinis to Azure AKS..."

# 1. Create resource group
echo "Creating resource group..."
az group create --name $RG --location $LOCATION

# 2. Create ACR
echo "Creating Azure Container Registry..."
az acr create --name $ACR_NAME --resource-group $RG --sku Basic

# 3. Create AKS
echo "Creating AKS cluster (this takes 10-15 minutes)..."
az aks create \
  --name $AKS_NAME \
  --resource-group $RG \
  --node-count 3 \
  --enable-managed-identity \
  --enable-addons monitoring \
  --enable-cluster-autoscaler \
  --min-count 1 \
  --max-count 5 \
  --attach-acr $ACR_NAME \
  --generate-ssh-keys

# 4. Get credentials
echo "Getting AKS credentials..."
az aks get-credentials --name $AKS_NAME --resource-group $RG

# 5. Import image
echo "Importing Docker image to ACR..."
az acr import \
  --name $ACR_NAME \
  --source docker.io/maurorisonho/houdinis:latest \
  --image houdinis:latest

# 6. Deploy to AKS
echo "Deploying to AKS..."
kubectl apply -f k8s/deployment-azure.yaml

# 7. Wait for deployment
echo "Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=houdinis -n houdinis --timeout=300s

# 8. Get service IP
echo "Getting service external IP..."
kubectl get svc -n houdinis

echo " Deployment complete!"
echo "Check status: kubectl get all -n houdinis"
```

---

## Next Steps

1. **Setup monitoring**: Configure Azure Monitor dashboards
2. **Enable auto-scaling**: HPA already configured
3. **Secure secrets**: Migrate to Key Vault
4. **Backup strategy**: Configure Blob Storage lifecycle
5. **DR plan**: Setup geo-replication

---

## Support

- **Documentation**: `/docs/README.md`
- **Issues**: https://github.com/maurorisonho/Houdinis/issues
- **Discord**: [Join our community](#)

**Deployment Status**: Production-Ready 
