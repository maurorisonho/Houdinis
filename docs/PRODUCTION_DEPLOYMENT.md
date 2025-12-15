# Production Deployment Guide - Houdinis Framework

Complete production deployment guide for Houdinis Quantum Cryptanalysis Framework across multiple cloud providers.

##  Table of Contents
- [Overview](#overview)
- [Quick Start](#quick-start)
- [Cloud Provider Guides](#cloud-provider-guides)
- [Container Registries](#container-registries)
- [Monitoring & Observability](#monitoring--observability)
- [Security Hardening](#security-hardening)
- [Scaling Strategies](#scaling-strategies)
- [Backup & Disaster Recovery](#backup--disaster-recovery)
- [Troubleshooting](#troubleshooting)
- [Cost Optimization](#cost-optimization)
- [Best Practices](#best-practices)

---

## Overview

### Architecture Patterns

Houdinis supports three deployment architectures:

1. **Serverless** (Recommended for variable workloads)
   - AWS: ECS Fargate, Lambda
   - Azure: Container Instances, Container Apps
   - GCP: Cloud Run

2. **Kubernetes** (Recommended for production)
   - AWS: EKS
   - Azure: AKS
   - GCP: GKE

3. **Virtual Machines** (Traditional approach)
   - AWS: EC2
   - Azure: VMs
   - GCP: Compute Engine

### Deployment Decision Matrix

| Criteria | Serverless | Kubernetes | VMs |
|----------|-----------|------------|-----|
| **Cost (low usage)** |  |  |  |
| **Cost (high usage)** |  |  |  |
| **Setup complexity** |  |  |  |
| **Scaling** |  |  |  |
| **Control** |  |  |  |
| **Cold starts** |  |  |  |

---

## Quick Start

### Prerequisites Checklist

- [ ] Cloud provider account (AWS/Azure/GCP)
- [ ] CLI tools installed (aws-cli, az, gcloud)
- [ ] kubectl installed (for Kubernetes deployments)
- [ ] Docker installed
- [ ] Git repository access
- [ ] IBM Quantum token (for quantum backends)

### 5-Minute Deployment

#### Option 1: Cloud Run (GCP) - Fastest
```bash
# Install gcloud SDK
curl https://sdk.cloud.google.com | bash

# Login and setup
gcloud init
gcloud auth login

# Deploy (one command!)
gcloud run deploy houdinis \
  --image maurorisonho/houdinis:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars PYTHONUNBUFFERED=1

# Get URL
gcloud run services list
```

#### Option 2: Azure Container Instances - Simple
```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login
az login

# Deploy
az container create \
  --name houdinis \
  --image maurorisonho/houdinis:latest \
  --resource-group houdinis-rg \
  --location eastus \
  --cpu 2 \
  --memory 4 \
  --ports 8000 \
  --dns-name-label houdinis-app

# Get FQDN
az container show --name houdinis --query ipAddress.fqdn
```

#### Option 3: AWS ECS Fargate - Scalable
```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip && sudo ./aws/install

# Configure
aws configure

# Use deployment script
cd docs/deployments
chmod +x deploy-aws-ecs.sh
./deploy-aws-ecs.sh
```

---

## Cloud Provider Guides

### Detailed Deployment Guides

| Cloud Provider | Guide | Best For |
|---------------|-------|----------|
| **AWS** | [`AWS_DEPLOYMENT.md`](./AWS_DEPLOYMENT.md) | Enterprise, complex infrastructure |
| **Azure** | [`AZURE_DEPLOYMENT.md`](./AZURE_DEPLOYMENT.md) | Microsoft ecosystem, hybrid cloud |
| **GCP** | [`GCP_DEPLOYMENT.md`](./GCP_DEPLOYMENT.md) | Simplicity, serverless, ML workloads |

Each guide includes:
-  Step-by-step instructions
-  Complete configuration examples
-  Troubleshooting section
-  Cost optimization tips
-  Security best practices

---

## Container Registries

### Docker Hub (Public)
```bash
# Pull latest image
docker pull maurorisonho/houdinis:latest

# Pull specific version
docker pull maurorisonho/houdinis:v1.0.0

# Pull vulnerable variant (for testing)
docker pull maurorisonho/houdinis:vulnerable
```

### GitHub Container Registry (GHCR)
```bash
# Pull from GHCR
docker pull ghcr.io/maurorisonho/houdinis:latest

# Authentication (for private repos)
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin
```

### Private Registry Setup

#### AWS ECR
```bash
# Create repository
aws ecr create-repository --repository-name houdinis

# Authenticate
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Tag and push
docker tag maurorisonho/houdinis:latest ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/houdinis:latest
docker push ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/houdinis:latest
```

#### Azure ACR
```bash
# Create registry
az acr create --name houdinisacr --sku Basic

# Login
az acr login --name houdinisacr

# Import from Docker Hub
az acr import \
  --name houdinisacr \
  --source docker.io/maurorisonho/houdinis:latest \
  --image houdinis:latest
```

#### GCP Artifact Registry
```bash
# Create repository
gcloud artifacts repositories create houdinis-repo \
  --repository-format docker \
  --location us-central1

# Tag and push
docker tag maurorisonho/houdinis:latest \
  us-central1-docker.pkg.dev/PROJECT_ID/houdinis-repo/houdinis:latest
docker push us-central1-docker.pkg.dev/PROJECT_ID/houdinis-repo/houdinis:latest
```

---

## Monitoring & Observability

### Complete Monitoring Stack

We provide a production-ready monitoring stack with:
- **Prometheus** - Metrics collection
- **Grafana** - Visualization dashboards
- **AlertManager** - Alert routing
- **ELK Stack** - Log aggregation (Elasticsearch, Logstash, Kibana)
- **Loki** - Cloud-native log aggregation
- **Jaeger** - Distributed tracing

### Quick Setup

```bash
cd monitoring

# Start entire stack
docker-compose up -d

# Access dashboards
open http://localhost:3000    # Grafana (admin/admin)
open http://localhost:9090    # Prometheus
open http://localhost:9093    # AlertManager
open http://localhost:5601    # Kibana
open http://localhost:16686   # Jaeger
```

### Grafana Dashboards

Pre-configured dashboards available at `/monitoring/grafana/dashboards/`:
- `houdinis-overview.json` - System overview
- `houdinis-performance.json` - Performance metrics
- `houdinis-quantum.json` - Quantum backend metrics
- `houdinis-exploits.json` - Exploit execution stats
- `kubernetes-cluster.json` - K8s cluster health

### Alert Rules

Alert rules configured in `/monitoring/prometheus/alert_rules.yml`:
- **Critical**: CPU > 95%, Memory > 95%, Service down
- **Warning**: CPU > 80%, Memory > 80%, High error rate
- **Custom**: Quantum backend failures, exploit execution failures

### Log Management

#### ELK Stack Configuration
```bash
# View Houdinis logs in Kibana
curl -X GET "localhost:9200/houdinis-*/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match": {
      "application": "houdinis"
    }
  }
}
'

# Search for errors
curl -X GET "localhost:9200/houdinis-errors-*/_search?pretty"
```

#### Loki Query Examples
```bash
# View all Houdinis logs
{app="houdinis"}

# Filter by log level
{app="houdinis"} |= "ERROR"

# Quantum backend logs
{app="houdinis"} |= "quantum_backend"

# Exploit execution logs
{app="houdinis", exploit!=""}
```

---

## Security Hardening

### Security Checklist

- [ ] **Secrets Management**: Use cloud provider secret services
- [ ] **Network Security**: Implement VPC/VNet with private subnets
- [ ] **Access Control**: Enable IAM/RBAC with least privilege
- [ ] **Encryption**: Enable encryption at rest and in transit
- [ ] **Vulnerability Scanning**: Regular container image scans
- [ ] **Audit Logging**: Enable comprehensive audit logs
- [ ] **WAF**: Deploy Web Application Firewall
- [ ] **DDoS Protection**: Enable cloud provider DDoS protection
- [ ] **Security Groups**: Restrict inbound traffic to necessary ports
- [ ] **Certificate Management**: Use managed certificates (Let's Encrypt, ACM)

### Secrets Management

#### AWS Secrets Manager
```bash
# Store secret
aws secretsmanager create-secret \
  --name houdinis/ibm-token \
  --secret-string "YOUR_IBM_TOKEN"

# Retrieve secret in application
aws secretsmanager get-secret-value --secret-id houdinis/ibm-token
```

#### Azure Key Vault
```bash
# Create Key Vault
az keyvault create --name houdinis-kv --resource-group houdinis-rg

# Store secret
az keyvault secret set --vault-name houdinis-kv --name ibm-token --value "YOUR_TOKEN"

# Retrieve secret
az keyvault secret show --vault-name houdinis-kv --name ibm-token
```

#### GCP Secret Manager
```bash
# Create secret
echo -n "YOUR_IBM_TOKEN" | gcloud secrets create ibm-token --data-file=-

# Access secret
gcloud secrets versions access latest --secret="ibm-token"
```

### Network Security

#### VPC Configuration (AWS)
```bash
# Create VPC with private subnets
aws ec2 create-vpc --cidr-block 10.0.0.0/16
aws ec2 create-subnet --vpc-id vpc-xxx --cidr-block 10.0.1.0/24 --availability-zone us-east-1a
aws ec2 create-subnet --vpc-id vpc-xxx --cidr-block 10.0.2.0/24 --availability-zone us-east-1b

# Create NAT Gateway for outbound traffic
aws ec2 create-nat-gateway --subnet-id subnet-xxx --allocation-id eipalloc-xxx
```

#### Security Groups (AWS)
```bash
# Create security group
aws ec2 create-security-group \
  --group-name houdinis-sg \
  --description "Houdinis security group" \
  --vpc-id vpc-xxx

# Allow HTTPS only
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxx \
  --protocol tcp \
  --port 443 \
  --cidr 0.0.0.0/0
```

### WAF Configuration

#### AWS WAF
```bash
# Create web ACL
aws wafv2 create-web-acl \
  --name houdinis-waf \
  --scope REGIONAL \
  --default-action Allow={} \
  --rules file://waf-rules.json

# Associate with ALB
aws wafv2 associate-web-acl \
  --web-acl-arn arn:aws:wafv2:... \
  --resource-arn arn:aws:elasticloadbalancing:...
```

#### Azure WAF
```bash
# Create WAF policy
az network application-gateway waf-policy create \
  --name houdinis-waf \
  --resource-group houdinis-rg

# Configure rules
az network application-gateway waf-policy managed-rule rule-set add \
  --policy-name houdinis-waf \
  --type OWASP \
  --version 3.2
```

#### GCP Cloud Armor
```bash
# Create security policy
gcloud compute security-policies create houdinis-policy

# Add rate limiting
gcloud compute security-policies rules create 1000 \
  --security-policy houdinis-policy \
  --action rate-based-ban \
  --rate-limit-threshold-count 100 \
  --rate-limit-threshold-interval-sec 60
```

---

## Scaling Strategies

### Horizontal Pod Autoscaling (HPA)

**Kubernetes HPA Configuration:**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: houdinis-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: houdinis
  minReplicas: 2
  maxReplicas: 20
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
```

### Vertical Pod Autoscaling (VPA)

```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: houdinis-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: houdinis
  updatePolicy:
    updateMode: "Auto"
  resourcePolicy:
    containerPolicies:
    - containerName: houdinis
      minAllowed:
        cpu: 500m
        memory: 1Gi
      maxAllowed:
        cpu: 4000m
        memory: 8Gi
```

### Cluster Autoscaling

#### AWS EKS
```bash
# Install cluster autoscaler
kubectl apply -f https://raw.githubusercontent.com/kubernetes/autoscaler/master/cluster-autoscaler/cloudprovider/aws/examples/cluster-autoscaler-autodiscover.yaml

# Configure
kubectl -n kube-system annotate deployment.apps/cluster-autoscaler \
  cluster-autoscaler.kubernetes.io/safe-to-evict="false"
```

#### Azure AKS
```bash
# Enable cluster autoscaler
az aks update \
  --name houdinis-aks \
  --enable-cluster-autoscaler \
  --min-count 1 \
  --max-count 10
```

#### GCP GKE
```bash
# Update cluster with autoscaling
gcloud container clusters update houdinis-gke \
  --enable-autoscaling \
  --min-nodes 1 \
  --max-nodes 10 \
  --region us-central1
```

---

## Backup & Disaster Recovery

### Backup Strategy

| Component | Backup Frequency | Retention | Tool |
|-----------|-----------------|-----------|------|
| **Configuration** | On change | 90 days | Git |
| **Application State** | Hourly | 7 days | Cloud Storage |
| **Database** | Daily | 30 days | Cloud Backup |
| **Logs** | Real-time | 90 days | Log Aggregator |
| **Secrets** | On change | 365 days | Secret Manager |

### Kubernetes Backup with Velero

```bash
# Install Velero
velero install \
  --provider aws \
  --plugins velero/velero-plugin-for-aws:v1.8.0 \
  --bucket houdinis-backups \
  --backup-location-config region=us-east-1 \
  --snapshot-location-config region=us-east-1

# Create backup schedule
velero schedule create houdinis-daily \
  --schedule="0 2 * * *" \
  --include-namespaces houdinis \
  --ttl 720h

# Restore from backup
velero restore create --from-backup houdinis-daily-20250115
```

### Disaster Recovery Plan

#### RTO (Recovery Time Objective)
- **Critical**: < 1 hour
- **High**: < 4 hours
- **Medium**: < 24 hours

#### RPO (Recovery Point Objective)
- **Critical**: < 15 minutes
- **High**: < 1 hour
- **Medium**: < 24 hours

#### Multi-Region Deployment

**Active-Active Setup:**
```yaml
# Global load balancer configuration
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: houdinis-global
  annotations:
    kubernetes.io/ingress.global-static-ip-name: houdinis-global-ip
    ingress.gcp.kubernetes.io/multi-cluster: "true"
spec:
  rules:
  - host: houdinis.example.com
    http:
      paths:
      - path: /*
        backend:
          service:
            name: houdinis
            port:
              number: 80
```

---

## Troubleshooting

### Common Issues & Solutions

#### Issue 1: Container Fails to Start
```bash
# Check logs
kubectl logs -n houdinis POD_NAME --previous

# Check events
kubectl describe pod -n houdinis POD_NAME

# Common causes:
# - Missing secrets
# - Invalid configuration
# - Image pull errors
# - Resource limits too low
```

**Solution:**
```bash
# Verify secrets exist
kubectl get secrets -n houdinis

# Check resource quotas
kubectl describe resourcequota -n houdinis

# Verify image pull
kubectl run test --image=maurorisonho/houdinis:latest --rm -it --restart=Never -- /bin/bash
```

#### Issue 2: High Memory Usage
```bash
# Check memory metrics
kubectl top pods -n houdinis

# Describe pod
kubectl describe pod -n houdinis POD_NAME | grep -A 5 "Limits\|Requests"
```

**Solution:**
```yaml
# Increase memory limits
resources:
  requests:
    memory: 2Gi
  limits:
    memory: 4Gi
```

#### Issue 3: Connection Timeouts
```bash
# Test connectivity
kubectl run curl --image=curlimages/curl -it --rm --restart=Never -- \
  curl -v http://houdinis.houdinis.svc.cluster.local:8000

# Check service endpoints
kubectl get endpoints -n houdinis
```

**Solution:**
```bash
# Verify service selector matches pods
kubectl get pods -n houdinis --show-labels
kubectl describe service houdinis -n houdinis
```

### Debug Checklist

- [ ] Check pod status: `kubectl get pods -n houdinis`
- [ ] Review logs: `kubectl logs -n houdinis POD_NAME`
- [ ] Check events: `kubectl get events -n houdinis --sort-by='.lastTimestamp'`
- [ ] Verify secrets: `kubectl get secrets -n houdinis`
- [ ] Test connectivity: `kubectl exec -it POD_NAME -- /bin/bash`
- [ ] Check resource usage: `kubectl top pods -n houdinis`
- [ ] Review metrics: Check Grafana dashboards
- [ ] Verify configuration: `kubectl describe deployment houdinis -n houdinis`

---

## Cost Optimization

### Cloud Cost Comparison (Monthly Estimates)

| Workload Type | AWS | Azure | GCP |
|---------------|-----|-------|-----|
| **Low** (< 100 hrs/month) | $15-30 | $12-25 | $10-20 |
| **Medium** (< 500 hrs/month) | $75-150 | $65-130 | $55-110 |
| **High** (24/7) | $300-500 | $280-450 | $250-400 |

### Cost Optimization Strategies

#### 1. Right-sizing
```bash
# Analyze actual usage
kubectl top pods -n houdinis --containers

# Recommendations from VPA
kubectl describe vpa houdinis-vpa
```

#### 2. Spot/Preemptible Instances
```bash
# AWS Spot Instances (60-90% discount)
aws ecs update-service \
  --capacity-provider-strategy capacityProvider=FARGATE_SPOT,weight=1

# GCP Preemptible VMs (up to 80% discount)
gcloud container node-pools create spot-pool \
  --cluster houdinis-gke \
  --preemptible \
  --enable-autoscaling \
  --min-nodes 0 \
  --max-nodes 10
```

#### 3. Reserved Instances/Savings Plans
- **AWS**: 1-year (30% off), 3-year (60% off)
- **Azure**: 1-year (25% off), 3-year (50% off)
- **GCP**: 1-year (25% off), 3-year (52% off)

#### 4. Auto-scaling Configuration
```yaml
# Aggressive scale-down for cost savings
behavior:
  scaleDown:
    stabilizationWindowSeconds: 60  # Fast scale-down
    policies:
    - type: Percent
      value: 100
      periodSeconds: 15
```

#### 5. Shut Down Dev/Test Environments
```bash
# Stop development cluster nights/weekends
# AWS
aws ecs update-service --desired-count 0 --service dev-houdinis

# GCP Cloud Scheduler
gcloud scheduler jobs create app-engine scale-down \
  --schedule="0 18 * * 1-5" \
  --relative-url="/scale?count=0"
```

---

## Best Practices

### Production Readiness Checklist

#### Infrastructure
- [ ] Multi-AZ/multi-region deployment
- [ ] Load balancing configured
- [ ] Auto-scaling enabled (HPA + Cluster Autoscaler)
- [ ] Resource requests and limits set
- [ ] Health checks configured
- [ ] Readiness and liveness probes
- [ ] Network policies implemented

#### Security
- [ ] Secrets stored in managed service (not env vars)
- [ ] TLS/HTTPS enforced
- [ ] Network segmentation (VPC/VNet)
- [ ] RBAC/IAM configured with least privilege
- [ ] Container images scanned for vulnerabilities
- [ ] Security updates automated
- [ ] WAF deployed
- [ ] DDoS protection enabled

#### Monitoring & Logging
- [ ] Prometheus metrics collection
- [ ] Grafana dashboards configured
- [ ] Alert rules defined
- [ ] On-call rotation established
- [ ] Log aggregation (ELK/Loki)
- [ ] Distributed tracing (Jaeger)
- [ ] Uptime monitoring (external)
- [ ] SLO/SLA defined

#### Backup & DR
- [ ] Automated backups configured
- [ ] Backup restoration tested
- [ ] DR plan documented
- [ ] Multi-region failover tested
- [ ] RTO/RPO defined and measured

#### CI/CD
- [ ] Automated testing (unit, integration, E2E)
- [ ] Container image building automated
- [ ] Deployment automated
- [ ] Rollback procedure documented
- [ ] Blue-green or canary deployments
- [ ] GitOps workflow (ArgoCD/Flux)

### Deployment Best Practices

1. **Use GitOps**: Store all configuration in Git
2. **Immutable Infrastructure**: Never modify running containers
3. **12-Factor App**: Follow 12-factor methodology
4. **Progressive Delivery**: Canary/blue-green deployments
5. **Observability**: Metrics, logs, traces from day one
6. **Least Privilege**: Minimize permissions everywhere
7. **Documentation**: Keep runbooks up-to-date
8. **Testing**: Test in production-like environment
9. **Monitoring**: Monitor business metrics, not just infrastructure
10. **Incident Response**: Have playbooks for common issues

---

## Support & Resources

### Documentation
- **Main README**: `/README.md`
- **AWS Deployment**: `/docs/deployments/AWS_DEPLOYMENT.md`
- **Azure Deployment**: `/docs/deployments/AZURE_DEPLOYMENT.md`
- **GCP Deployment**: `/docs/deployments/GCP_DEPLOYMENT.md`
- **Security**: `/docs/SECURITY.md`
- **Architecture**: `/docs/PROJECT_STRUCTURE_ORGANIZATION.md`

### Community
- **GitHub Issues**: https://github.com/maurorisonho/Houdinis/issues
- **Discussions**: https://github.com/maurorisonho/Houdinis/discussions
- **Discord**: Coming soon
- **Twitter**: @HoudinisFramework (planned)

### Commercial Support
- **Email**: support@houdinis.io (planned)
- **Enterprise Support**: Available for production deployments

---

## Deployment Status

| Component | Status | Version |
|-----------|--------|---------|
| **Docker Images** |  Published | latest, v1.0.0 |
| **AWS Deployment** |  Complete | ECS, EKS, EC2 |
| **Azure Deployment** |  Complete | ACI, AKS, VMs |
| **GCP Deployment** |  Complete | Cloud Run, GKE, Compute Engine |
| **Monitoring Stack** |  Complete | Prometheus, Grafana, ELK |
| **CI/CD Pipeline** |  Complete | GitHub Actions |
| **Security Hardening** |  Complete | WAF, Secrets, RBAC |

---

**Last Updated**: December 15, 2025  
**Version**: 1.0.0  
**Status**: Production-Ready 
