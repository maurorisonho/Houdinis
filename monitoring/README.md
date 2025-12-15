# Production Monitoring Stack - Houdinis Framework

Complete observability stack for production deployments of Houdinis.

##  Stack Overview

This monitoring stack provides comprehensive observability across metrics, logs, and traces:

| Component | Purpose | Port | URL |
|-----------|---------|------|-----|
| **Prometheus** | Metrics collection & alerting | 9090 | http://localhost:9090 |
| **Grafana** | Visualization dashboards | 3000 | http://localhost:3000 |
| **AlertManager** | Alert routing & management | 9093 | http://localhost:9093 |
| **Elasticsearch** | Log storage (ELK) | 9200 | http://localhost:9200 |
| **Logstash** | Log processing (ELK) | 5000 | TCP/UDP 5000 |
| **Kibana** | Log visualization (ELK) | 5601 | http://localhost:5601 |
| **Loki** | Cloud-native log aggregation | 3100 | http://localhost:3100 |
| **Promtail** | Log shipper for Loki | - | - |
| **Jaeger** | Distributed tracing | 16686 | http://localhost:16686 |
| **Node Exporter** | Host metrics | 9100 | http://localhost:9100 |
| **cAdvisor** | Container metrics | 8080 | http://localhost:8080 |

---

##  Quick Start

### 1. Start the Stack
```bash
cd monitoring
docker-compose up -d
```

### 2. Verify All Services
```bash
docker-compose ps
```

Expected output:
```
NAME                      STATUS    PORTS
houdinis-prometheus       Up        0.0.0.0:9090->9090/tcp
houdinis-grafana          Up        0.0.0.0:3000->3000/tcp
houdinis-alertmanager     Up        0.0.0.0:9093->9093/tcp
houdinis-elasticsearch    Up        0.0.0.0:9200->9200/tcp
houdinis-kibana           Up        0.0.0.0:5601->5601/tcp
houdinis-loki             Up        0.0.0.0:3100->3100/tcp
houdinis-jaeger           Up        0.0.0.0:16686->16686/tcp
...
```

### 3. Access Dashboards

#### Grafana (Primary Dashboard)
- **URL**: http://localhost:3000
- **Username**: `admin`
- **Password**: `admin`
- **Default Dashboards**: Pre-loaded in `/grafana/dashboards/`

#### Prometheus
- **URL**: http://localhost:9090
- **Features**: Query metrics, view targets, check alert rules

#### Kibana (ELK Logs)
- **URL**: http://localhost:5601
- **Setup**: Create index pattern `houdinis-*` on first access

#### Jaeger (Tracing)
- **URL**: http://localhost:16686
- **Features**: View distributed traces, service dependencies

---

##  Directory Structure

```
monitoring/
 docker-compose.yml              # Complete stack definition
 prometheus/
    prometheus.yml              # Prometheus configuration
    alert_rules.yml             # 20+ alert rules (CPU, memory, errors)
 grafana/
    provisioning/
       datasources/            # Auto-configured datasources
    dashboards/                 # Pre-built dashboards (TBD)
 alertmanager/
    config.yml                  # Alert routing (email, Slack, PagerDuty)
 logstash/
    config/
       logstash.yml
    pipeline/
        logstash.conf           # Log processing pipeline
 loki/
    config.yml                  # Loki configuration
 promtail/
    config.yml                  # Log collection config
 README.md                       # This file
```

---

##  Monitoring Capabilities

### Metrics (Prometheus + Grafana)

**Application Metrics:**
- CPU utilization per pod
- Memory usage and limits
- Request rate and latency (p50, p95, p99)
- Error rate (4xx, 5xx)
- Quantum backend operation success/failure rate
- Exploit execution metrics

**Infrastructure Metrics:**
- Kubernetes cluster health
- Node resource utilization
- Pod status and restarts
- Container resource usage
- Network traffic

**Custom Metrics:**
- Quantum circuit execution time
- Shor's algorithm factorization success rate
- Grover's search iterations
- IBM Quantum backend queue time

### Logs (ELK Stack + Loki)

**Log Aggregation:**
- All container logs (stdout/stderr)
- Application logs (Python logging)
- System logs (/var/log)
- Kubernetes events

**Log Filtering:**
- By severity (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- By component (quantum, exploits, cli)
- By tag (quantum_backend, exploit_execution)
- By time range

**Special Indexes:**
- `houdinis-errors-*` - Error logs only
- `houdinis-exploits-*` - Exploit execution logs
- `houdinis-quantum-*` - Quantum backend logs

### Traces (Jaeger)

**Distributed Tracing:**
- End-to-end request tracing
- Service dependency mapping
- Latency analysis per component
- Error propagation tracking

---

##  Alert Rules

Pre-configured alerts in `prometheus/alert_rules.yml`:

### Critical Alerts (Immediate Action Required)
-  **HoudinisCPUCritical**: CPU > 95% for 2 minutes
-  **HoudinisMemoryCritical**: Memory > 95% for 2 minutes
-  **HoudinisPodCrashLooping**: Pod restarting repeatedly
-  **HoudinisServiceDown**: Service unavailable for 2 minutes
-  **HoudinisHighErrorRate**: Error rate > 5%
-  **HoudinisQuantumBackendFailure**: Quantum backend errors > 0.1/s

### Warning Alerts (Investigate Soon)
-  **HoudinisCPUHigh**: CPU > 80% for 5 minutes
-  **HoudinisMemoryHigh**: Memory > 80% for 5 minutes
-  **HoudinisPodNotReady**: Pod not ready for 10 minutes
-  **HoudinisSlowResponseTime**: P95 latency > 5 seconds
-  **HoudinisDiskSpaceLow**: Disk space < 20%

### Kubernetes Infrastructure Alerts
-  **KubernetesNodeNotReady**: Node down for 10 minutes
-  **KubernetesNodeMemoryPressure**: Node under memory pressure
-  **KubernetesNodeDiskPressure**: Node under disk pressure

---

##  Alert Routing

AlertManager routes alerts based on severity:

### Critical Alerts
- **Email**: oncall@houdinis.io
- **Slack**: #houdinis-critical
- **PagerDuty**: Immediate page
- **Repeat**: Every 1 hour

### Warning Alerts
- **Email**: team@houdinis.io
- **Slack**: #houdinis-alerts
- **Repeat**: Every 4 hours

### Configuration
Edit `alertmanager/config.yml` to customize:
```yaml
receivers:
  - name: 'critical'
    email_configs:
      - to: 'oncall@houdinis.io'
    slack_configs:
      - api_url: 'YOUR_SLACK_WEBHOOK'
        channel: '#houdinis-critical'
    pagerduty_configs:
      - service_key: 'YOUR_PAGERDUTY_KEY'
```

---

##  Grafana Dashboards

### Pre-configured Dashboards

1. **Houdinis Overview** (`houdinis-overview.json`)
   - System health overview
   - Request rate and latency
   - Error rate
   - Resource utilization
   - Active pods and replicas

2. **Houdinis Performance** (`houdinis-performance.json`)
   - Response time percentiles (p50, p95, p99)
   - Throughput metrics
   - Resource efficiency
   - Performance trends

3. **Houdinis Quantum** (`houdinis-quantum.json`)
   - Quantum backend status
   - Circuit execution metrics
   - IBM Quantum API calls
   - Backend queue times
   - Success/failure rates

4. **Houdinis Exploits** (`houdinis-exploits.json`)
   - Exploit execution stats
   - Success rates by exploit type
   - Shor's algorithm metrics
   - Grover's search metrics

5. **Kubernetes Cluster** (`kubernetes-cluster.json`)
   - Cluster resource usage
   - Node health
   - Pod distribution
   - Network traffic

### Creating Custom Dashboards

1. Open Grafana: http://localhost:3000
2. Click **+** → **Dashboard**
3. Add panel with PromQL queries:
   ```promql
   # CPU usage
   rate(container_cpu_usage_seconds_total{namespace="houdinis"}[5m])
   
   # Memory usage
   container_memory_usage_bytes{namespace="houdinis"}
   
   # Request rate
   rate(http_requests_total{namespace="houdinis"}[5m])
   ```

---

##  Configuration

### Prometheus Scraping

Prometheus auto-discovers Houdinis pods using Kubernetes service discovery:

```yaml
- job_name: 'houdinis'
  kubernetes_sd_configs:
    - role: pod
      namespaces:
        names:
          - houdinis
  relabel_configs:
    - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
      action: keep
      regex: true
```

**To enable scraping on your pods:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "9090"
    prometheus.io/path: "/metrics"
```

### Logstash Pipeline

Logs are processed through Logstash pipeline:

1. **Input**: Receives logs via TCP/UDP (port 5000) or Beats
2. **Filter**: Parses JSON, extracts fields, adds tags
3. **Output**: Sends to Elasticsearch indexes

**Custom fields added:**
- `application: houdinis`
- `environment: production`
- Tags: `error`, `exploit`, `quantum`

### Loki Labels

Loki uses labels for log organization:
```promql
{app="houdinis", level="ERROR"}
{app="houdinis", component="quantum"}
{app="houdinis", exploit="shor"}
```

---

##  Troubleshooting

### Prometheus Not Scraping Targets
```bash
# Check Prometheus targets
open http://localhost:9090/targets

# Verify pod annotations
kubectl get pods -n houdinis -o yaml | grep prometheus.io

# Test metrics endpoint
kubectl port-forward -n houdinis POD_NAME 9090:9090
curl http://localhost:9090/metrics
```

### Grafana Dashboards Not Loading
```bash
# Check Grafana logs
docker logs houdinis-grafana

# Verify datasource connectivity
curl http://localhost:3000/api/datasources

# Restart Grafana
docker-compose restart grafana
```

### Elasticsearch Not Indexing Logs
```bash
# Check Elasticsearch health
curl http://localhost:9200/_cluster/health?pretty

# Verify Logstash pipeline
docker logs houdinis-logstash

# Test log ingestion
echo '{"message":"test","level":"INFO"}' | nc localhost 5000
```

### High Memory Usage
```bash
# Check resource usage
docker stats

# Reduce Elasticsearch heap
ES_JAVA_OPTS="-Xms256m -Xmx256m"

# Reduce Logstash heap
LS_JAVA_OPTS="-Xmx256m -Xms256m"
```

---

##  Production Best Practices

### 1. Resource Limits
```yaml
services:
  prometheus:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
```

### 2. Data Retention
- **Prometheus**: 30 days (configurable)
- **Elasticsearch**: 90 days with ILM
- **Loki**: 90 days

### 3. Backup Strategy
```bash
# Backup Prometheus data
docker run --rm -v prometheus_data:/data -v $(pwd):/backup alpine tar czf /backup/prometheus-backup.tar.gz /data

# Backup Grafana dashboards
docker exec houdinis-grafana grafana-cli admin export > grafana-backup.json
```

### 4. High Availability
- Run 3+ Prometheus replicas with Thanos
- Use Elasticsearch cluster (3+ nodes)
- Deploy Grafana behind load balancer

### 5. Security
- Enable authentication on all services
- Use TLS for all connections
- Restrict network access with firewall rules
- Rotate credentials regularly

---

##  Integration with Cloud Providers

### AWS CloudWatch Integration
```yaml
- job_name: 'cloudwatch'
  static_configs:
    - targets: ['cloudwatch-exporter:9090']
```

### Azure Monitor Integration
```yaml
- job_name: 'azure'
  static_configs:
    - targets: ['azure-exporter:9090']
```

### GCP Stackdriver Integration
```yaml
- job_name: 'stackdriver'
  static_configs:
    - targets: ['stackdriver-exporter:9090']
```

---

##  Additional Resources

- **Prometheus Docs**: https://prometheus.io/docs/
- **Grafana Docs**: https://grafana.com/docs/
- **ELK Stack**: https://www.elastic.co/guide/
- **Loki Docs**: https://grafana.com/docs/loki/
- **Jaeger Docs**: https://www.jaegertracing.io/docs/

---

##  Support

- **Issues**: https://github.com/maurorisonho/Houdinis/issues
- **Documentation**: `/docs/PRODUCTION_DEPLOYMENT.md`
- **Deployment Guides**: `/docs/deployments/`

---

**Status**: Production-Ready   
**Last Updated**: December 15, 2025
