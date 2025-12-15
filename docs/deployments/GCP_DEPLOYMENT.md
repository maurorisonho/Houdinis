# Google Cloud Platform Deployment Guide

Complete guide for deploying Houdinis Framework on Google Cloud Platform (GCP).

## Table of Contents
- [Architecture Overview](#architecture-overview)
- [Prerequisites](#prerequisites)
- [Deployment Options](#deployment-options)
  - [Cloud Run (Serverless)](#cloud-run-deployment)
  - [GKE (Google Kubernetes Engine)](#gke-deployment)
  - [Compute Engine with Docker](#compute-engine-deployment)
- [Configuration](#configuration)
- [Monitoring](#monitoring)
- [Scaling](#scaling)
- [Security](#security)
- [Troubleshooting](#troubleshooting)
- [Cost Optimization](#cost-optimization)

---

## Architecture Overview

```

                    Google Cloud Platform                    
                                                             
                
  Cloud DNS   Cloud Load    Cloud        
                    Balancer            Armor (WAF)  
                
                                                           
                                                           
                                        
                     Cloud Run/GKE                        
                       Cluster                            
                                        
                   /       |        \                       
                        
         Service 1   Service2  Service 3            
         Houdinis                                   
                        
                                                             
       
  Cloud       Cloud        Secret Manager           
  Storage     Logging      API Keys/Credentials     
       

```

---

## Prerequisites

### gcloud CLI
```bash
# Install gcloud SDK
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Initialize and authenticate
gcloud init
gcloud auth login
gcloud auth application-default login

# Set project
gcloud config set project YOUR_PROJECT_ID

# Verify
gcloud config list
```

### Enable APIs
```bash
# Enable required APIs
gcloud services enable \
  run.googleapis.com \
  container.googleapis.com \
  containerregistry.googleapis.com \
  artifactregistry.googleapis.com \
  compute.googleapis.com \
  cloudresourcemanager.googleapis.com \
  secretmanager.googleapis.com \
  monitoring.googleapis.com \
  logging.googleapis.com
```

### Install Tools
```bash
# kubectl
gcloud components install kubectl

# GKE auth plugin
gcloud components install gke-gcloud-auth-plugin

# Docker credential helper
gcloud components install docker-credential-gcr
```

---

## Deployment Options

### Cloud Run Deployment

Cloud Run is the fastest, most cost-effective option for serverless containers.

#### 1. Quick Start
```bash
# Deploy directly from Docker Hub
gcloud run deploy houdinis \
  --image maurorisonho/houdinis:latest \
  --platform managed \
  --region us-central1 \
  --port 8000 \
  --cpu 2 \
  --memory 4Gi \
  --min-instances 1 \
  --max-instances 10 \
  --timeout 300 \
  --concurrency 100 \
  --allow-unauthenticated \
  --set-env-vars PYTHONUNBUFFERED=1,LOG_LEVEL=INFO \
  --set-secrets IBM_QUANTUM_TOKEN=ibm-token:latest

# Get URL
gcloud run services describe houdinis \
  --region us-central1 \
  --format 'value(status.url)'

# View logs
gcloud run services logs tail houdinis --region us-central1
```

#### 2. Deploy with YAML
**cloudrun-service.yaml:**
```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: houdinis
  namespace: default
  labels:
    cloud.googleapis.com/location: us-central1
  annotations:
    run.googleapis.com/launch-stage: BETA
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: '1'
        autoscaling.knative.dev/maxScale: '10'
        run.googleapis.com/execution-environment: gen2
        run.googleapis.com/cpu-throttling: 'false'
        run.googleapis.com/startup-cpu-boost: 'true'
    spec:
      serviceAccountName: houdinis-sa@PROJECT_ID.iam.gserviceaccount.com
      timeoutSeconds: 300
      containerConcurrency: 100
      containers:
      - name: houdinis
        image: maurorisonho/houdinis:latest
        ports:
        - name: http1
          containerPort: 8000
        env:
        - name: PYTHONUNBUFFERED
          value: "1"
        - name: LOG_LEVEL
          value: INFO
        - name: GCP_PROJECT
          value: YOUR_PROJECT_ID
        - name: IBM_QUANTUM_TOKEN
          valueFrom:
            secretKeyRef:
              name: ibm-token
              key: latest
        resources:
          limits:
            cpu: '2'
            memory: 4Gi
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 10
        startupProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 0
          periodSeconds: 1
          failureThreshold: 30
  traffic:
  - percent: 100
    latestRevision: true
```

Deploy:
```bash
gcloud run services replace cloudrun-service.yaml --region us-central1
```

#### 3. Setup Cloud Storage for Persistence
```bash
# Create bucket
gcloud storage buckets create gs://houdinis-output \
  --location us-central1 \
  --uniform-bucket-level-access

# Grant service account access
gcloud storage buckets add-iam-policy-binding gs://houdinis-output \
  --member serviceAccount:houdinis-sa@PROJECT_ID.iam.gserviceaccount.com \
  --role roles/storage.objectAdmin

# Mount in Cloud Run (via code)
# Install google-cloud-storage in requirements.txt
```

---

### GKE Deployment

Google Kubernetes Engine (GKE) for production workloads.

#### 1. Create GKE Cluster
```bash
# Create Autopilot cluster (recommended)
gcloud container clusters create-auto houdinis-gke \
  --region us-central1 \
  --release-channel regular \
  --enable-autoscaling \
  --min-nodes 1 \
  --max-nodes 10

# OR create Standard cluster (more control)
gcloud container clusters create houdinis-gke \
  --region us-central1 \
  --num-nodes 3 \
  --machine-type n1-standard-2 \
  --enable-autoscaling \
  --min-nodes 1 \
  --max-nodes 10 \
  --enable-autorepair \
  --enable-autoupgrade \
  --enable-stackdriver-kubernetes \
  --addons HorizontalPodAutoscaling,HttpLoadBalancing,GcePersistentDiskCsiDriver

# Get credentials
gcloud container clusters get-credentials houdinis-gke --region us-central1

# Verify
kubectl get nodes
```

#### 2. Create Artifact Registry
```bash
# Create registry
gcloud artifacts repositories create houdinis-repo \
  --repository-format docker \
  --location us-central1 \
  --description "Houdinis container images"

# Configure Docker authentication
gcloud auth configure-docker us-central1-docker.pkg.dev

# Tag and push image
docker tag maurorisonho/houdinis:latest \
  us-central1-docker.pkg.dev/PROJECT_ID/houdinis-repo/houdinis:latest

docker push us-central1-docker.pkg.dev/PROJECT_ID/houdinis-repo/houdinis:latest
```

#### 3. Deploy to GKE
**k8s/deployment-gcp.yaml:**
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
  GCP_PROJECT: "YOUR_PROJECT_ID"
  GCP_REGION: "us-central1"
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
apiVersion: v1
kind: ServiceAccount
metadata:
  name: houdinis
  namespace: houdinis
  annotations:
    iam.gke.io/gcp-service-account: houdinis-sa@PROJECT_ID.iam.gserviceaccount.com
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
        image: us-central1-docker.pkg.dev/PROJECT_ID/houdinis-repo/houdinis:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 8000
          name: http
          protocol: TCP
        - containerPort: 9090
          name: metrics
          protocol: TCP
        env:
        - name: GOOGLE_APPLICATION_CREDENTIALS
          value: /var/secrets/google/key.json
        envFrom:
        - configMapRef:
            name: houdinis-config
        - secretRef:
            name: houdinis-secrets
        resources:
          requests:
            cpu: 500m
            memory: 1Gi
            ephemeral-storage: 1Gi
          limits:
            cpu: 2000m
            memory: 4Gi
            ephemeral-storage: 5Gi
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
        volumeMounts:
        - name: output
          mountPath: /app/output
        - name: gcp-credentials
          mountPath: /var/secrets/google
          readOnly: true
      volumes:
      - name: output
        persistentVolumeClaim:
          claimName: houdinis-pvc
      - name: gcp-credentials
        secret:
          secretName: gcp-service-account-key
---
apiVersion: v1
kind: Service
metadata:
  name: houdinis
  namespace: houdinis
  annotations:
    cloud.google.com/neg: '{"ingress": true}'
    cloud.google.com/backend-config: '{"default": "houdinis-backend-config"}'
spec:
  type: LoadBalancer
  selector:
    app: houdinis
  ports:
  - port: 80
    targetPort: 8000
    protocol: TCP
    name: http
  - port: 9090
    targetPort: 9090
    protocol: TCP
    name: metrics
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
---
apiVersion: cloud.google.com/v1
kind: BackendConfig
metadata:
  name: houdinis-backend-config
  namespace: houdinis
spec:
  healthCheck:
    checkIntervalSec: 10
    port: 8000
    type: HTTP
    requestPath: /health
  connectionDraining:
    drainingTimeoutSec: 60
  timeoutSec: 300
  logging:
    enable: true
    sampleRate: 1.0
  iap:
    enabled: false
```

Deploy:
```bash
# Apply manifests
kubectl apply -f k8s/deployment-gcp.yaml

# Verify deployment
kubectl get all -n houdinis

# Get external IP
kubectl get svc -n houdinis

# View logs
kubectl logs -n houdinis -l app=houdinis --tail=100 -f
```

#### 4. Setup Ingress with Google Cloud Load Balancer
```bash
# Reserve static IP
gcloud compute addresses create houdinis-ip --global

# Get IP address
gcloud compute addresses describe houdinis-ip --global --format="value(address)"
```

**k8s/ingress-gcp.yaml:**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: houdinis-ingress
  namespace: houdinis
  annotations:
    kubernetes.io/ingress.class: "gce"
    kubernetes.io/ingress.global-static-ip-name: "houdinis-ip"
    networking.gke.io/managed-certificates: "houdinis-cert"
    kubernetes.io/ingress.allow-http: "true"
spec:
  rules:
  - host: houdinis.example.com
    http:
      paths:
      - path: /*
        pathType: ImplementationSpecific
        backend:
          service:
            name: houdinis
            port:
              number: 80
---
apiVersion: networking.gke.io/v1
kind: ManagedCertificate
metadata:
  name: houdinis-cert
  namespace: houdinis
spec:
  domains:
  - houdinis.example.com
```

Apply:
```bash
kubectl apply -f k8s/ingress-gcp.yaml

# Wait for certificate provisioning (10-20 minutes)
kubectl describe managedcertificate houdinis-cert -n houdinis
```

---

### Compute Engine Deployment

#### 1. Create VM Instance
```bash
# Create instance with container-optimized OS
gcloud compute instances create-with-container houdinis-vm \
  --zone us-central1-a \
  --machine-type n1-standard-2 \
  --container-image maurorisonho/houdinis:latest \
  --container-restart-policy always \
  --container-env PYTHONUNBUFFERED=1,LOG_LEVEL=INFO \
  --container-mount-host-path mount-path=/app/output,host-path=/data/houdinis,mode=rw \
  --tags http-server \
  --boot-disk-size 50GB \
  --metadata-from-file startup-script=startup.sh

# Create firewall rule
gcloud compute firewall-rules create allow-houdinis \
  --allow tcp:8000 \
  --target-tags http-server \
  --description "Allow access to Houdinis on port 8000"

# Get external IP
gcloud compute instances describe houdinis-vm \
  --zone us-central1-a \
  --format='get(networkInterfaces[0].accessConfigs[0].natIP)'
```

**startup.sh:**
```bash
#!/bin/bash
set -e

# Update system
apt-get update
apt-get install -y docker.io google-cloud-ops-agent

# Configure Cloud Logging
cat > /etc/google-cloud-ops-agent/config.yaml <<EOF
logging:
  receivers:
    syslog:
      type: files
      include_paths:
      - /var/log/docker/*.log
  processors:
    parse_json:
      type: parse_json
      field: message
  exporters:
    google:
      type: google_cloud_logging
  service:
    pipelines:
      default_pipeline:
        receivers: [syslog]
        processors: [parse_json]
        exporters: [google]
EOF

systemctl restart google-cloud-ops-agent

# Pull and run container
docker pull maurorisonho/houdinis:latest
docker run -d \
  --name houdinis \
  --restart unless-stopped \
  -p 8000:8000 \
  -v /data/houdinis:/app/output \
  -e PYTHONUNBUFFERED=1 \
  -e LOG_LEVEL=INFO \
  maurorisonho/houdinis:latest

echo " Houdinis deployed successfully!"
```

#### 2. Setup Managed Instance Group (for scaling)
```bash
# Create instance template
gcloud compute instance-templates create-with-container houdinis-template \
  --machine-type n1-standard-2 \
  --container-image maurorisonho/houdinis:latest \
  --container-restart-policy always \
  --tags http-server \
  --boot-disk-size 50GB

# Create managed instance group
gcloud compute instance-groups managed create houdinis-mig \
  --base-instance-name houdinis \
  --template houdinis-template \
  --size 3 \
  --region us-central1

# Setup autoscaling
gcloud compute instance-groups managed set-autoscaling houdinis-mig \
  --region us-central1 \
  --min-num-replicas 1 \
  --max-num-replicas 10 \
  --target-cpu-utilization 0.7 \
  --cool-down-period 60

# Create health check
gcloud compute health-checks create http houdinis-health-check \
  --port 8000 \
  --request-path /health \
  --check-interval 10s

# Set named port
gcloud compute instance-groups managed set-named-ports houdinis-mig \
  --region us-central1 \
  --named-ports http:8000

# Create backend service
gcloud compute backend-services create houdinis-backend \
  --protocol HTTP \
  --health-checks houdinis-health-check \
  --global

# Add instance group to backend
gcloud compute backend-services add-backend houdinis-backend \
  --instance-group houdinis-mig \
  --instance-group-region us-central1 \
  --global
```

---

## Configuration

### Secret Manager
```bash
# Create secret
echo -n "YOUR_IBM_TOKEN" | gcloud secrets create ibm-token \
  --data-file=- \
  --replication-policy automatic

# Grant Cloud Run access
gcloud secrets add-iam-policy-binding ibm-token \
  --member serviceAccount:houdinis-sa@PROJECT_ID.iam.gserviceaccount.com \
  --role roles/secretmanager.secretAccessor

# Grant GKE access (Workload Identity)
gcloud iam service-accounts add-iam-policy-binding \
  houdinis-sa@PROJECT_ID.iam.gserviceaccount.com \
  --role roles/iam.workloadIdentityUser \
  --member "serviceAccount:PROJECT_ID.svc.id.goog[houdinis/houdinis]"
```

### Environment Variables
```bash
# Update Cloud Run with new env vars
gcloud run services update houdinis \
  --region us-central1 \
  --set-env-vars NEW_VAR=value

# Update GKE deployment
kubectl set env deployment/houdinis -n houdinis NEW_VAR=value
```

---

## Monitoring

### Cloud Monitoring Dashboard
```bash
# Create custom dashboard
gcloud monitoring dashboards create --config-from-file dashboard.json
```

**dashboard.json:**
```json
{
  "displayName": "Houdinis Monitoring",
  "mosaicLayout": {
    "columns": 12,
    "tiles": [
      {
        "width": 6,
        "height": 4,
        "widget": {
          "title": "Cloud Run CPU Utilization",
          "xyChart": {
            "dataSets": [{
              "timeSeriesQuery": {
                "timeSeriesFilter": {
                  "filter": "resource.type=\"cloud_run_revision\" resource.labels.service_name=\"houdinis\"",
                  "aggregation": {
                    "alignmentPeriod": "60s",
                    "perSeriesAligner": "ALIGN_RATE"
                  }
                }
              }
            }]
          }
        }
      },
      {
        "xPos": 6,
        "width": 6,
        "height": 4,
        "widget": {
          "title": "Memory Usage",
          "xyChart": {
            "dataSets": [{
              "timeSeriesQuery": {
                "timeSeriesFilter": {
                  "filter": "resource.type=\"cloud_run_revision\" resource.labels.service_name=\"houdinis\" metric.type=\"run.googleapis.com/container/memory/utilizations\"",
                  "aggregation": {
                    "alignmentPeriod": "60s",
                    "perSeriesAligner": "ALIGN_MEAN"
                  }
                }
              }
            }]
          }
        }
      }
    ]
  }
}
```

### Cloud Logging Queries
```bash
# View all logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=houdinis" \
  --limit 50 \
  --format json

# Filter errors
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=houdinis AND severity>=ERROR" \
  --limit 20 \
  --format json

# Stream logs
gcloud logging tail "resource.type=cloud_run_revision AND resource.labels.service_name=houdinis"
```

### Alert Policies
```bash
# Create alert for high CPU
gcloud alpha monitoring policies create \
  --notification-channels=CHANNEL_ID \
  --display-name="Houdinis High CPU" \
  --condition-display-name="CPU > 80%" \
  --condition-threshold-value=0.8 \
  --condition-threshold-duration=300s \
  --condition-expression='
    resource.type = "cloud_run_revision"
    AND resource.labels.service_name = "houdinis"
    AND metric.type = "run.googleapis.com/container/cpu/utilizations"
  '
```

---

## Scaling

### Cloud Run Auto-scaling
```bash
# Update scaling configuration
gcloud run services update houdinis \
  --region us-central1 \
  --min-instances 2 \
  --max-instances 20 \
  --concurrency 100

# Enable CPU boost for cold starts
gcloud run services update houdinis \
  --region us-central1 \
  --cpu-boost
```

### GKE Node Auto-scaling
```bash
# Enable cluster autoscaler
gcloud container clusters update houdinis-gke \
  --enable-autoscaling \
  --min-nodes 1 \
  --max-nodes 10 \
  --region us-central1

# Update node pool
gcloud container node-pools update default-pool \
  --cluster houdinis-gke \
  --enable-autoscaling \
  --min-nodes 2 \
  --max-nodes 20 \
  --region us-central1
```

---

## Security

### Cloud Armor (WAF)
```bash
# Create security policy
gcloud compute security-policies create houdinis-policy \
  --description "Security policy for Houdinis"

# Add rate limiting rule
gcloud compute security-policies rules create 1000 \
  --security-policy houdinis-policy \
  --expression "true" \
  --action "rate-based-ban" \
  --rate-limit-threshold-count 100 \
  --rate-limit-threshold-interval-sec 60 \
  --ban-duration-sec 600

# Add geo-blocking rule
gcloud compute security-policies rules create 2000 \
  --security-policy houdinis-policy \
  --expression "origin.region_code == 'CN'" \
  --action "deny-403"

# Attach to backend service
gcloud compute backend-services update houdinis-backend \
  --security-policy houdinis-policy \
  --global
```

### VPC Service Controls
```bash
# Create perimeter
gcloud access-context-manager perimeters create houdinis-perimeter \
  --title "Houdinis Security Perimeter" \
  --resources "projects/PROJECT_NUMBER" \
  --restricted-services "run.googleapis.com,container.googleapis.com" \
  --policy POLICY_ID
```

---

## Troubleshooting

### Cloud Run Issues
```bash
# View service details
gcloud run services describe houdinis --region us-central1

# Check revisions
gcloud run revisions list --service houdinis --region us-central1

# View logs with errors only
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=houdinis AND severity>=ERROR" --limit 20

# Rollback to previous revision
gcloud run services update-traffic houdinis \
  --to-revisions PREVIOUS_REVISION=100 \
  --region us-central1
```

### GKE Issues
```bash
# Check cluster status
gcloud container clusters describe houdinis-gke --region us-central1

# List nodes
kubectl get nodes -o wide

# Check pod logs
kubectl logs -n houdinis -l app=houdinis --tail=100

# Describe pod
kubectl describe pod POD_NAME -n houdinis

# Check events
kubectl get events -n houdinis --sort-by='.lastTimestamp'

# Debug with ephemeral container
kubectl debug -it POD_NAME -n houdinis --image=busybox
```

---

## Cost Optimization

### Cloud Run Pricing
- **CPU**: $0.00002400/vCPU-second
- **Memory**: $0.00000250/GiB-second
- **Requests**: $0.40 per million requests
- **Free tier**: 2M requests/month, 360K vCPU-seconds, 180K GiB-seconds

**Optimization tips:**
```bash
# Use minimum instances only when needed
gcloud run services update houdinis --min-instances 0

# Optimize CPU allocation
gcloud run services update houdinis --cpu 1

# Use gen2 execution environment
gcloud run services update houdinis --execution-environment gen2
```

### GKE Spot VMs
```bash
# Create spot node pool
gcloud container node-pools create spot-pool \
  --cluster houdinis-gke \
  --spot \
  --enable-autoscaling \
  --num-nodes 1 \
  --min-nodes 0 \
  --max-nodes 10 \
  --machine-type n1-standard-2 \
  --region us-central1
```

### Committed Use Discounts
- 1-year: ~25% discount
- 3-year: ~52% discount

### Cost Monitoring
```bash
# Export billing to BigQuery
gcloud beta billing accounts set-export \
  --account-id BILLING_ACCOUNT_ID \
  --destination-dataset-id billing_export \
  --destination-project-id PROJECT_ID

# Query costs
bq query --use_legacy_sql=false '
SELECT
  service.description,
  SUM(cost) as total_cost
FROM `PROJECT_ID.billing_export.gcp_billing_export_v1_*`
WHERE _TABLE_SUFFIX BETWEEN "20250101" AND "20250131"
  AND project.id = "PROJECT_ID"
GROUP BY service.description
ORDER BY total_cost DESC
'
```

---

## Complete Deployment Script

**deploy-gcp-cloudrun.sh:**
```bash
#!/bin/bash
set -e

PROJECT_ID="YOUR_PROJECT_ID"
REGION="us-central1"
SERVICE_NAME="houdinis"

echo " Deploying Houdinis to Google Cloud Run..."

# 1. Set project
gcloud config set project $PROJECT_ID

# 2. Enable APIs
echo "Enabling required APIs..."
gcloud services enable run.googleapis.com secretmanager.googleapis.com

# 3. Create service account
echo "Creating service account..."
gcloud iam service-accounts create houdinis-sa \
  --display-name "Houdinis Service Account" || true

# 4. Create secret (if needed)
if ! gcloud secrets describe ibm-token &>/dev/null; then
  echo "Creating secret..."
  echo -n "YOUR_IBM_TOKEN" | gcloud secrets create ibm-token --data-file=-
fi

# 5. Grant secret access
echo "Granting secret access..."
gcloud secrets add-iam-policy-binding ibm-token \
  --member serviceAccount:houdinis-sa@$PROJECT_ID.iam.gserviceaccount.com \
  --role roles/secretmanager.secretAccessor

# 6. Deploy Cloud Run service
echo "Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image maurorisonho/houdinis:latest \
  --platform managed \
  --region $REGION \
  --service-account houdinis-sa@$PROJECT_ID.iam.gserviceaccount.com \
  --port 8000 \
  --cpu 2 \
  --memory 4Gi \
  --min-instances 1 \
  --max-instances 10 \
  --timeout 300 \
  --concurrency 100 \
  --allow-unauthenticated \
  --set-env-vars PYTHONUNBUFFERED=1,LOG_LEVEL=INFO,GCP_PROJECT=$PROJECT_ID \
  --set-secrets IBM_QUANTUM_TOKEN=ibm-token:latest

# 7. Get service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME \
  --region $REGION \
  --format 'value(status.url)')

echo " Deployment complete!"
echo "Service URL: $SERVICE_URL"
echo "View logs: gcloud run services logs tail $SERVICE_NAME --region $REGION"
```

---

## Next Steps

1. **Setup monitoring**: Configure Cloud Monitoring dashboards
2. **Enable auto-scaling**: Already configured in Cloud Run/GKE
3. **Secure secrets**: Migrate to Secret Manager 
4. **Backup strategy**: Configure Cloud Storage lifecycle
5. **DR plan**: Setup multi-region deployment

---

## Support

- **Documentation**: `/docs/README.md`
- **Issues**: https://github.com/maurorisonho/Houdinis/issues
- **Discord**: [Join our community](#)

**Deployment Status**: Production-Ready 
