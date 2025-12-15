# AWS Deployment Guide

Complete guide for deploying Houdinis Framework on Amazon Web Services (AWS).

## Table of Contents
- [Architecture Overview](#architecture-overview)
- [Prerequisites](#prerequisites)
- [Deployment Options](#deployment-options)
  - [ECS (Elastic Container Service)](#ecs-deployment)
  - [EKS (Elastic Kubernetes Service)](#eks-deployment)
  - [EC2 with Docker](#ec2-deployment)
- [Configuration](#configuration)
- [Monitoring](#monitoring)
- [Scaling](#scaling)
- [Security](#security)
- [Troubleshooting](#troubleshooting)
- [Cost Optimization](#cost-optimization)

---

## Architecture Overview

```

                         AWS Cloud                        
                                                          
               
    Route 53   Load Balancer   WAF    
               
                                                         
                                                         
                                        
                      ECS/EKS                           
                      Cluster                           
                                        
                   /      |      \                        
                           
           Task 1   Task 2    Task 3              
          Houdinis                                
                           
                                                          
          
     S3        CloudWatch    Secrets Manager     
   Storage        Logs         API Keys/Creds    
          

```

---

## Prerequisites

### AWS CLI
```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configure credentials
aws configure
# AWS Access Key ID: YOUR_ACCESS_KEY
# AWS Secret Access Key: YOUR_SECRET_KEY
# Default region: us-east-1
# Default output format: json
```

### IAM Permissions
Required IAM policies:
- `AmazonECS_FullAccess` or `AmazonEKS_FullAccess`
- `AmazonEC2ContainerRegistryFullAccess`
- `CloudWatchLogsFullAccess`
- `SecretsManagerReadWrite`
- `AmazonS3FullAccess`

### Tools
```bash
# ECS CLI
sudo curl -Lo /usr/local/bin/ecs-cli https://amazon-ecs-cli.s3.amazonaws.com/ecs-cli-linux-amd64-latest
sudo chmod +x /usr/local/bin/ecs-cli

# eksctl (for EKS)
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin

# kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

---

## Deployment Options

### ECS Deployment

#### 1. Create ECS Cluster
```bash
# Create cluster
aws ecs create-cluster --cluster-name houdinis-cluster

# Create task execution role (if not exists)
aws iam create-role --role-name ecsTaskExecutionRole \
  --assume-role-policy-document file://ecs-trust-policy.json

# Attach required policies
aws iam attach-role-policy --role-name ecsTaskExecutionRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
```

**ecs-trust-policy.json:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

#### 2. Create Task Definition
```bash
aws ecs register-task-definition --cli-input-json file://houdinis-task-definition.json
```

**houdinis-task-definition.json:**
```json
{
  "family": "houdinis-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::ACCOUNT_ID:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::ACCOUNT_ID:role/ecsTaskRole",
  "containerDefinitions": [
    {
      "name": "houdinis",
      "image": "maurorisonho/houdinis:latest",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "PYTHONUNBUFFERED",
          "value": "1"
        },
        {
          "name": "LOG_LEVEL",
          "value": "INFO"
        }
      ],
      "secrets": [
        {
          "name": "IBM_QUANTUM_TOKEN",
          "valueFrom": "arn:aws:secretsmanager:REGION:ACCOUNT_ID:secret:houdinis/ibm-token"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/houdinis",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "houdinis"
        }
      },
      "healthCheck": {
        "command": ["CMD-SHELL", "python -c 'import sys; sys.exit(0)'"],
        "interval": 30,
        "timeout": 5,
        "retries": 3,
        "startPeriod": 60
      }
    }
  ]
}
```

#### 3. Create Service
```bash
# Create CloudWatch log group
aws logs create-log-group --log-group-name /ecs/houdinis

# Create service
aws ecs create-service \
  --cluster houdinis-cluster \
  --service-name houdinis-service \
  --task-definition houdinis-task \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxxxx,subnet-yyyyy],securityGroups=[sg-xxxxx],assignPublicIp=ENABLED}" \
  --load-balancers "targetGroupArn=arn:aws:elasticloadbalancing:REGION:ACCOUNT_ID:targetgroup/houdinis-tg/xxx,containerName=houdinis,containerPort=8000"
```

#### 4. Create Application Load Balancer (Optional)
```bash
# Create ALB
aws elbv2 create-load-balancer \
  --name houdinis-alb \
  --subnets subnet-xxxxx subnet-yyyyy \
  --security-groups sg-xxxxx \
  --scheme internet-facing \
  --type application

# Create target group
aws elbv2 create-target-group \
  --name houdinis-tg \
  --protocol HTTP \
  --port 8000 \
  --vpc-id vpc-xxxxx \
  --target-type ip \
  --health-check-path /health \
  --health-check-interval-seconds 30

# Create listener
aws elbv2 create-listener \
  --load-balancer-arn arn:aws:elasticloadbalancing:REGION:ACCOUNT_ID:loadbalancer/app/houdinis-alb/xxx \
  --protocol HTTP \
  --port 80 \
  --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:REGION:ACCOUNT_ID:targetgroup/houdinis-tg/xxx
```

---

### EKS Deployment

#### 1. Create EKS Cluster
```bash
# Create cluster (15-20 minutes)
eksctl create cluster \
  --name houdinis-eks \
  --region us-east-1 \
  --nodegroup-name standard-workers \
  --node-type t3.medium \
  --nodes 3 \
  --nodes-min 1 \
  --nodes-max 5 \
  --managed

# Update kubeconfig
aws eks update-kubeconfig --region us-east-1 --name houdinis-eks
```

#### 2. Deploy to EKS
```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml

# Verify deployment
kubectl get pods -n houdinis
kubectl get svc -n houdinis
```

**k8s/deployment-aws.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: houdinis
  namespace: houdinis
  labels:
    app: houdinis
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
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "9090"
    spec:
      serviceAccountName: houdinis
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      containers:
      - name: houdinis
        image: maurorisonho/houdinis:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 8000
          name: http
          protocol: TCP
        env:
        - name: PYTHONUNBUFFERED
          value: "1"
        - name: LOG_LEVEL
          value: "INFO"
        - name: AWS_REGION
          value: "us-east-1"
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
          successThreshold: 1
        volumeMounts:
        - name: output
          mountPath: /app/output
        - name: config
          mountPath: /app/config
      volumes:
      - name: output
        persistentVolumeClaim:
          claimName: houdinis-output-pvc
      - name: config
        configMap:
          name: houdinis-config-files
---
apiVersion: v1
kind: Service
metadata:
  name: houdinis
  namespace: houdinis
spec:
  type: LoadBalancer
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: nlb
    service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
  selector:
    app: houdinis
  ports:
  - port: 80
    targetPort: 8000
    protocol: TCP
    name: http
```

#### 3. Setup Auto-scaling
```bash
# Install metrics server
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Create HPA
kubectl autoscale deployment houdinis \
  --namespace houdinis \
  --cpu-percent=70 \
  --min=2 \
  --max=10

# Verify HPA
kubectl get hpa -n houdinis
```

---

### EC2 Deployment

#### 1. Launch EC2 Instance
```bash
# Create security group
aws ec2 create-security-group \
  --group-name houdinis-sg \
  --description "Security group for Houdinis"

# Allow SSH
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxx \
  --protocol tcp \
  --port 22 \
  --cidr 0.0.0.0/0

# Allow HTTP
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxx \
  --protocol tcp \
  --port 8000 \
  --cidr 0.0.0.0/0

# Launch instance
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --count 1 \
  --instance-type t3.medium \
  --key-name YOUR_KEY_PAIR \
  --security-group-ids sg-xxxxx \
  --subnet-id subnet-xxxxx \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=houdinis-server}]' \
  --user-data file://user-data.sh
```

**user-data.sh:**
```bash
#!/bin/bash
set -e

# Update system
yum update -y

# Install Docker
yum install -y docker
systemctl start docker
systemctl enable docker
usermod -a -G docker ec2-user

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Pull and run Houdinis
docker pull maurorisonho/houdinis:latest
docker run -d \
  --name houdinis \
  --restart unless-stopped \
  -p 8000:8000 \
  -v /data/houdinis:/app/output \
  -e LOG_LEVEL=INFO \
  maurorisonho/houdinis:latest

# Install CloudWatch agent
wget https://s3.amazonaws.com/amazoncloudwatch-agent/amazon_linux/amd64/latest/amazon-cloudwatch-agent.rpm
rpm -U ./amazon-cloudwatch-agent.rpm

# Configure CloudWatch logs
cat > /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json <<EOF
{
  "logs": {
    "logs_collected": {
      "files": {
        "collect_list": [
          {
            "file_path": "/var/log/docker/*.log",
            "log_group_name": "/aws/ec2/houdinis",
            "log_stream_name": "{instance_id}"
          }
        ]
      }
    }
  }
}
EOF

/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
  -a fetch-config \
  -m ec2 \
  -s \
  -c file:/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json
```

#### 2. Connect and Verify
```bash
# SSH to instance
ssh -i your-key.pem ec2-user@ec2-xxx.compute.amazonaws.com

# Check container
docker ps
docker logs houdinis

# Test application
curl http://localhost:8000/health
```

---

## Configuration

### Environment Variables
```bash
# Set in ECS task definition or Kubernetes secrets
PYTHONUNBUFFERED=1
LOG_LEVEL=INFO
QUANTUM_BACKEND=ibm
IBM_QUANTUM_TOKEN=your_token_here
AWS_REGION=us-east-1
S3_BUCKET=houdinis-output
```

### AWS Secrets Manager
```bash
# Store IBM Quantum token
aws secretsmanager create-secret \
  --name houdinis/ibm-token \
  --description "IBM Quantum token for Houdinis" \
  --secret-string "YOUR_IBM_TOKEN"

# Store other secrets
aws secretsmanager create-secret \
  --name houdinis/api-keys \
  --secret-string '{"aws":"xxx","azure":"yyy","google":"zzz"}'

# Grant ECS task access
aws iam attach-role-policy \
  --role-name ecsTaskRole \
  --policy-arn arn:aws:iam::aws:policy/SecretsManagerReadWrite
```

---

## Monitoring

### CloudWatch Metrics
```bash
# Create dashboard
aws cloudwatch put-dashboard \
  --dashboard-name Houdinis \
  --dashboard-body file://cloudwatch-dashboard.json
```

**cloudwatch-dashboard.json:**
```json
{
  "widgets": [
    {
      "type": "metric",
      "properties": {
        "metrics": [
          ["AWS/ECS", "CPUUtilization", {"stat": "Average"}],
          [".", "MemoryUtilization", {"stat": "Average"}]
        ],
        "period": 300,
        "stat": "Average",
        "region": "us-east-1",
        "title": "ECS Resource Utilization"
      }
    },
    {
      "type": "log",
      "properties": {
        "query": "SOURCE '/ecs/houdinis' | fields @timestamp, @message | filter @message like /ERROR/ | sort @timestamp desc | limit 20",
        "region": "us-east-1",
        "title": "Recent Errors"
      }
    }
  ]
}
```

### CloudWatch Alarms
```bash
# CPU alarm
aws cloudwatch put-metric-alarm \
  --alarm-name houdinis-high-cpu \
  --alarm-description "Alert when CPU exceeds 80%" \
  --metric-name CPUUtilization \
  --namespace AWS/ECS \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2 \
  --alarm-actions arn:aws:sns:us-east-1:ACCOUNT_ID:houdinis-alerts

# Memory alarm
aws cloudwatch put-metric-alarm \
  --alarm-name houdinis-high-memory \
  --alarm-description "Alert when memory exceeds 80%" \
  --metric-name MemoryUtilization \
  --namespace AWS/ECS \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2 \
  --alarm-actions arn:aws:sns:us-east-1:ACCOUNT_ID:houdinis-alerts
```

---

## Scaling

### ECS Auto-scaling
```bash
# Register scalable target
aws application-autoscaling register-scalable-target \
  --service-namespace ecs \
  --resource-id service/houdinis-cluster/houdinis-service \
  --scalable-dimension ecs:service:DesiredCount \
  --min-capacity 2 \
  --max-capacity 10

# Create scaling policy
aws application-autoscaling put-scaling-policy \
  --service-namespace ecs \
  --resource-id service/houdinis-cluster/houdinis-service \
  --scalable-dimension ecs:service:DesiredCount \
  --policy-name houdinis-cpu-scaling \
  --policy-type TargetTrackingScaling \
  --target-tracking-scaling-policy-configuration file://scaling-policy.json
```

**scaling-policy.json:**
```json
{
  "TargetValue": 70.0,
  "PredefinedMetricSpecification": {
    "PredefinedMetricType": "ECSServiceAverageCPUUtilization"
  },
  "ScaleInCooldown": 300,
  "ScaleOutCooldown": 60
}
```

---

## Security

### Security Best Practices
1. **Use VPC with private subnets**
2. **Enable WAF on ALB**
3. **Rotate secrets regularly**
4. **Enable CloudTrail logging**
5. **Use IAM roles (not access keys)**
6. **Enable container image scanning**

### Security Group Configuration
```bash
# Restrict access to known IPs
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxx \
  --protocol tcp \
  --port 8000 \
  --cidr YOUR_IP/32
```

---

## Troubleshooting

### Common Issues

#### 1. Task fails to start
```bash
# Check task logs
aws ecs describe-tasks --cluster houdinis-cluster --tasks TASK_ID

# View CloudWatch logs
aws logs tail /ecs/houdinis --follow
```

#### 2. Container health check failing
```bash
# Exec into container
aws ecs execute-command \
  --cluster houdinis-cluster \
  --task TASK_ID \
  --container houdinis \
  --interactive \
  --command "/bin/bash"

# Check application
python -c "from core import cli; print('OK')"
```

#### 3. High memory usage
```bash
# Check memory metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/ECS \
  --metric-name MemoryUtilization \
  --dimensions Name=ServiceName,Value=houdinis-service \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Average
```

---

## Cost Optimization

### Fargate Spot
```bash
# Update service to use Fargate Spot
aws ecs update-service \
  --cluster houdinis-cluster \
  --service houdinis-service \
  --capacity-provider-strategy \
    capacityProvider=FARGATE_SPOT,weight=1,base=0 \
    capacityProvider=FARGATE,weight=0,base=1
```

### Reserved Instances (for EC2)
- Use Reserved Instances for predictable workloads
- 1-year term: ~30% discount
- 3-year term: ~60% discount

### Cost Monitoring
```bash
# Enable Cost Explorer
aws ce get-cost-and-usage \
  --time-period Start=2025-01-01,End=2025-01-31 \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --filter file://cost-filter.json
```

---

## Complete Deployment Script

**deploy-aws-ecs.sh:**
```bash
#!/bin/bash
set -e

CLUSTER_NAME="houdinis-cluster"
SERVICE_NAME="houdinis-service"
TASK_FAMILY="houdinis-task"
REGION="us-east-1"

echo " Deploying Houdinis to AWS ECS..."

# 1. Create cluster
echo "Creating ECS cluster..."
aws ecs create-cluster --cluster-name $CLUSTER_NAME --region $REGION || true

# 2. Register task definition
echo "Registering task definition..."
aws ecs register-task-definition --cli-input-json file://houdinis-task-definition.json --region $REGION

# 3. Create log group
echo "Creating CloudWatch log group..."
aws logs create-log-group --log-group-name /ecs/houdinis --region $REGION || true

# 4. Create or update service
echo "Creating/updating service..."
if aws ecs describe-services --cluster $CLUSTER_NAME --services $SERVICE_NAME --region $REGION | grep -q "ACTIVE"; then
  aws ecs update-service \
    --cluster $CLUSTER_NAME \
    --service $SERVICE_NAME \
    --task-definition $TASK_FAMILY \
    --desired-count 2 \
    --region $REGION
else
  aws ecs create-service \
    --cluster $CLUSTER_NAME \
    --service-name $SERVICE_NAME \
    --task-definition $TASK_FAMILY \
    --desired-count 2 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[subnet-xxxxx],securityGroups=[sg-xxxxx],assignPublicIp=ENABLED}" \
    --region $REGION
fi

echo " Deployment complete!"
echo "Check status: aws ecs describe-services --cluster $CLUSTER_NAME --services $SERVICE_NAME --region $REGION"
```

---

## Next Steps

1. **Setup monitoring**: Configure CloudWatch dashboards
2. **Enable auto-scaling**: Implement HPA or ECS auto-scaling
3. **Secure secrets**: Migrate to AWS Secrets Manager
4. **Backup strategy**: Configure S3 lifecycle policies
5. **DR plan**: Setup cross-region replication

---

## Support

- **Documentation**: `/docs/README.md`
- **Issues**: https://github.com/maurorisonho/Houdinis/issues
- **Discord**: [Join our community](#)

**Deployment Status**: Production-Ready 
