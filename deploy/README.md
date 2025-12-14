# Houdinis Framework - Cloud Deployment Guide

This directory contains deployment configurations for running Houdinis in various cloud environments.

## Table of Contents

- [Kubernetes Deployment](#kubernetes-deployment)
- [Helm Charts](#helm-charts)
- [Cloud Providers](#cloud-providers)
  - [AWS](#amazon-web-services-aws)
  - [Azure](#microsoft-azure)
  - [Google Cloud](#google-cloud-platform-gcp)
- [Security Considerations](#security-considerations)

## Kubernetes Deployment

### Prerequisites

- Kubernetes cluster (1.24+)
- kubectl configured
- Container registry access

### Quick Start

```bash
# Apply Kubernetes manifests
kubectl apply -f deploy/kubernetes/deployment.yaml

# Check deployment status
kubectl get pods -n houdinis
kubectl logs -f deployment/houdinis-framework -n houdinis

# Access the framework
kubectl exec -it deployment/houdinis-framework -n houdinis -- bash
```

### Configuration

Edit `deploy/kubernetes/deployment.yaml` to configure:
- Resource limits (CPU/Memory)
- Replica count
- Environment variables
- Secrets

### Secrets Management

```bash
# Create secrets from files
kubectl create secret generic houdinis-secrets \
  --from-literal=IBM_QUANTUM_TOKEN=your_token_here \
  --from-literal=AWS_ACCESS_KEY_ID=your_key_here \
  -n houdinis

# Or use a secrets file
kubectl create secret generic houdinis-secrets \
  --from-env-file=.env.secrets \
  -n houdinis
```

## Helm Charts

### Installation

```bash
# Add Houdinis Helm repository (when available)
helm repo add houdinis https://charts.houdinis-framework.org
helm repo update

# Or install from local chart
cd deploy/helm
helm install houdinis ./houdinis -n houdinis --create-namespace
```

### Configuration

Create a `values.yaml` file:

```yaml
replicaCount: 1

image:
  repository: ghcr.io/maurorisonho/houdinis
  tag: "latest"

resources:
  limits:
    cpu: 2000m
    memory: 4Gi
  requests:
    cpu: 1000m
    memory: 2Gi

houdinis:
  config:
    quantumBackend: "ibm_quantum"
  secrets:
    ibmQuantumToken: "your_base64_encoded_token"
```

Install with custom values:

```bash
helm install houdinis ./houdinis -f values.yaml -n houdinis
```

### Upgrading

```bash
helm upgrade houdinis ./houdinis -f values.yaml -n houdinis
```

### Uninstalling

```bash
helm uninstall houdinis -n houdinis
```

## Cloud Providers

### Amazon Web Services (AWS)

#### EKS Deployment

```bash
# Create EKS cluster
eksctl create cluster \
  --name houdinis-cluster \
  --region us-east-1 \
  --nodegroup-name houdinis-nodes \
  --node-type t3.xlarge \
  --nodes 2 \
  --nodes-min 1 \
  --nodes-max 5

# Configure kubectl
aws eks update-kubeconfig --name houdinis-cluster --region us-east-1

# Deploy Houdinis
kubectl apply -f deploy/kubernetes/deployment.yaml
```

#### AWS Braket Integration

Configure AWS Braket access:

```bash
kubectl create secret generic aws-braket-credentials \
  --from-literal=AWS_ACCESS_KEY_ID=your_key \
  --from-literal=AWS_SECRET_ACCESS_KEY=your_secret \
  --from-literal=AWS_DEFAULT_REGION=us-east-1 \
  -n houdinis
```

Update deployment to use AWS Braket:

```yaml
env:
- name: QUANTUM_BACKEND
  value: "aws_braket"
- name: AWS_ACCESS_KEY_ID
  valueFrom:
    secretKeyRef:
      name: aws-braket-credentials
      key: AWS_ACCESS_KEY_ID
```

#### Cost Optimization

- Use Spot Instances for worker nodes
- Set resource requests/limits appropriately
- Enable cluster autoscaling
- Use AWS Savings Plans

### Microsoft Azure

#### AKS Deployment

```bash
# Create resource group
az group create --name houdinis-rg --location eastus

# Create AKS cluster
az aks create \
  --resource-group houdinis-rg \
  --name houdinis-cluster \
  --node-count 2 \
  --node-vm-size Standard_D4s_v3 \
  --enable-managed-identity \
  --generate-ssh-keys

# Get credentials
az aks get-credentials --resource-group houdinis-rg --name houdinis-cluster

# Deploy Houdinis
kubectl apply -f deploy/kubernetes/deployment.yaml
```

#### Azure Quantum Integration

```bash
# Create Azure Quantum workspace
az quantum workspace create \
  --resource-group houdinis-rg \
  --name houdinis-quantum \
  --location eastus

# Configure secrets
kubectl create secret generic azure-quantum-credentials \
  --from-literal=AZURE_QUANTUM_SUBSCRIPTION=your_subscription_id \
  --from-literal=AZURE_QUANTUM_WORKSPACE=houdinis-quantum \
  --from-literal=AZURE_QUANTUM_RESOURCE_GROUP=houdinis-rg \
  -n houdinis
```

#### Azure Key Vault Integration

```bash
# Install Azure Key Vault CSI driver
helm repo add csi-secrets-store-provider-azure https://azure.github.io/secrets-store-csi-driver-provider-azure/charts
helm install csi csi-secrets-store-provider-azure/csi-secrets-store-provider-azure

# Configure SecretProviderClass
kubectl apply -f deploy/azure/secret-provider.yaml
```

### Google Cloud Platform (GCP)

#### GKE Deployment

```bash
# Create GKE cluster
gcloud container clusters create houdinis-cluster \
  --region us-central1 \
  --num-nodes 2 \
  --machine-type n1-standard-4 \
  --enable-autoscaling \
  --min-nodes 1 \
  --max-nodes 5

# Get credentials
gcloud container clusters get-credentials houdinis-cluster --region us-central1

# Deploy Houdinis
kubectl apply -f deploy/kubernetes/deployment.yaml
```

#### Google Quantum AI Integration

```bash
# Create service account
gcloud iam service-accounts create houdinis-quantum

# Grant permissions
gcloud projects add-iam-policy-binding your-project-id \
  --member="serviceAccount:houdinis-quantum@your-project-id.iam.gserviceaccount.com" \
  --role="roles/quantum.user"

# Create key
gcloud iam service-accounts keys create key.json \
  --iam-account=houdinis-quantum@your-project-id.iam.gserviceaccount.com

# Create Kubernetes secret
kubectl create secret generic google-quantum-credentials \
  --from-file=credentials.json=key.json \
  -n houdinis
```

#### Workload Identity

```bash
# Enable Workload Identity
gcloud container clusters update houdinis-cluster \
  --workload-pool=your-project-id.svc.id.goog

# Configure service account
kubectl annotate serviceaccount houdinis \
  iam.gke.io/gcp-service-account=houdinis-quantum@your-project-id.iam.gserviceaccount.com \
  -n houdinis
```

## Security Considerations

### Network Policies

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: houdinis-network-policy
  namespace: houdinis
spec:
  podSelector:
    matchLabels:
      app: houdinis
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - namespaceSelector: {}
    ports:
    - protocol: TCP
      port: 443  # HTTPS to quantum backends
```

### Pod Security Standards

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: houdinis
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

### Resource Quotas

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: houdinis-quota
  namespace: houdinis
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    pods: "10"
```

### RBAC

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind:Role
metadata:
  name: houdinis-role
  namespace: houdinis
rules:
- apiGroups: [""]
  resources: ["pods", "configmaps", "secrets"]
  verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: houdinis-rolebinding
  namespace: houdinis
subjects:
- kind: ServiceAccount
  name: houdinis
  namespace: houdinis
roleRef:
  kind: Role
  name: houdinis-role
  apiGroup: rbac.authorization.k8s.io
```

## Monitoring & Logging

### Prometheus Metrics

```yaml
apiVersion: v1
kind: Service
metadata:
  name: houdinis-metrics
  namespace: houdinis
  labels:
    app: houdinis
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "9090"
spec:
  ports:
  - name: metrics
    port: 9090
    targetPort: 9090
  selector:
    app: houdinis
```

### Log Aggregation

Use EFK Stack (Elasticsearch, Fluentd, Kibana) or ELK Stack:

```bash
# Deploy Fluentd DaemonSet
kubectl apply -f https://raw.githubusercontent.com/fluent/fluentd-kubernetes-daemonset/master/fluentd-daemonset-elasticsearch.yaml
```

## Scaling

### Horizontal Pod Autoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: houdinis-hpa
  namespace: houdinis
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: houdinis-framework
  minReplicas: 1
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
```

## Troubleshooting

### Check Pod Status

```bash
kubectl get pods -n houdinis
kubectl describe pod <pod-name> -n houdinis
kubectl logs <pod-name> -n houdinis
```

### Debug Container

```bash
kubectl run -it --rm debug --image=busybox --restart=Never -n houdinis -- sh
```

### Network Connectivity

```bash
kubectl run -it --rm nettest --image=nicolaka/netshoot --restart=Never -n houdinis -- bash
```

## Support

For deployment issues:
- GitHub Issues: https://github.com/maurorisonho/Houdinis/issues
- Documentation: https://houdinis-framework.org/docs
- Community Discord: [link]

## License

MIT License - See LICENSE file for details
