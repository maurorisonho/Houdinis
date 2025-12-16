#!/usr/bin/env python3
"""
# Houdinis Framework - Quantum Cryptography Testing Platform
# Author: Mauro Risonho de Paula Assumpção aka firebitsbr
# Developed by: Human Logic & Coding with AI Assistance (Claude Sonnet 4.5)
# License: MIT

Production-ready monitoring with Prometheus metrics, health checks, and observability.
Data de Criação: 15 de dezembro de 2025
"""

import time
import psutil
import os
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from datetime import datetime
import json
from pathlib import Path


try:
    from prometheus_client import Counter, Gauge, Histogram, Summary, Info, start_http_server, REGISTRY
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False
    print("[!] prometheus_client not available. Install with: pip install prometheus-client")


@dataclass
class HealthStatus:
    """Health check status."""
    healthy: bool
    status: str  # "healthy", "degraded", "unhealthy"
    timestamp: float
    checks: Dict[str, bool] = field(default_factory=dict)
    messages: List[str] = field(default_factory=list)


class PrometheusMetrics:
    """
    Prometheus metrics collection for Houdinis framework.
    
    Tracks:
    - Algorithm execution metrics
    - System resource usage
    - Quantum backend performance
    - Error rates and latencies
    """
    
    def __init__(self, port: int = 8000, enable_server: bool = False) -> None:
        """
        Initialize Prometheus metrics.
        
        Args:
            port: Port for metrics HTTP server
            enable_server: Whether to start HTTP server
        """
        self.port = port
        self.metrics_enabled = PROMETHEUS_AVAILABLE
        
        if not self.metrics_enabled:
            print("[!] Prometheus metrics disabled (library not available)")
            return
        
        # Algorithm execution metrics
        self.algorithm_executions = Counter(
            'houdinis_algorithm_executions_total',
            'Total number of algorithm executions',
            ['algorithm', 'backend', 'status']
        )
        
        self.algorithm_duration = Histogram(
            'houdinis_algorithm_duration_seconds',
            'Algorithm execution duration in seconds',
            ['algorithm', 'backend'],
            buckets=[0.1, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0, 120.0]
        )
        
        self.quantum_circuit_depth = Histogram(
            'houdinis_quantum_circuit_depth',
            'Quantum circuit depth',
            ['algorithm'],
            buckets=[10, 25, 50, 100, 250, 500, 1000, 2500]
        )
        
        # System metrics
        self.cpu_usage = Gauge(
            'houdinis_cpu_usage_percent',
            'CPU usage percentage'
        )
        
        self.memory_usage = Gauge(
            'houdinis_memory_usage_bytes',
            'Memory usage in bytes'
        )
        
        self.memory_usage_percent = Gauge(
            'houdinis_memory_usage_percent',
            'Memory usage percentage'
        )
        
        # Quantum backend metrics
        self.backend_requests = Counter(
            'houdinis_backend_requests_total',
            'Total backend requests',
            ['backend', 'status']
        )
        
        self.backend_latency = Summary(
            'houdinis_backend_latency_seconds',
            'Backend request latency',
            ['backend']
        )
        
        # Error metrics
        self.errors = Counter(
            'houdinis_errors_total',
            'Total errors',
            ['error_type', 'component']
        )
        
        # Security metrics
        self.security_scans = Counter(
            'houdinis_security_scans_total',
            'Total security scans',
            ['scan_type']
        )
        
        self.vulnerabilities_found = Gauge(
            'houdinis_vulnerabilities_found',
            'Number of vulnerabilities found',
            ['severity']
        )
        
        # Application info
        self.app_info = Info(
            'houdinis_application',
            'Application information'
        )
        self.app_info.info({
            'version': '1.0.0',
            'framework': 'Houdinis Quantum Cryptanalysis',
            'author': 'firebitsbr'
        })
        
        # Start metrics server if enabled
        if enable_server:
            self.start_server()
    
    def start_server(self) -> None:
        """Start Prometheus HTTP metrics server."""
        if not self.metrics_enabled:
            return
        
        try:
            start_http_server(self.port)
            print(f"[+] Prometheus metrics server started on port {self.port}")
            print(f"[+] Metrics available at: http://localhost:{self.port}/metrics")
        except Exception as e:
            print(f"[!] Failed to start metrics server: {e}")
    
    def record_algorithm_execution(
        self,
        algorithm: str,
        backend: str,
        duration: float,
        success: bool,
        circuit_depth: Optional[int] = None
    ) -> None:
        """
        Record algorithm execution metrics.
        
        Args:
            algorithm: Algorithm name
            backend: Backend used
            duration: Execution duration in seconds
            success: Whether execution succeeded
            circuit_depth: Optional circuit depth
        """
        if not self.metrics_enabled:
            return
        
        status = "success" if success else "failure"
        
        self.algorithm_executions.labels(
            algorithm=algorithm,
            backend=backend,
            status=status
        ).inc()
        
        self.algorithm_duration.labels(
            algorithm=algorithm,
            backend=backend
        ).observe(duration)
        
        if circuit_depth is not None:
            self.quantum_circuit_depth.labels(
                algorithm=algorithm
            ).observe(circuit_depth)
    
    def record_backend_request(
        self,
        backend: str,
        latency: float,
        success: bool
    ) -> None:
        """
        Record backend request metrics.
        
        Args:
            backend: Backend name
            latency: Request latency in seconds
            success: Whether request succeeded
        """
        if not self.metrics_enabled:
            return
        
        status = "success" if success else "failure"
        
        self.backend_requests.labels(
            backend=backend,
            status=status
        ).inc()
        
        self.backend_latency.labels(backend=backend).observe(latency)
    
    def record_error(self, error_type: str, component: str) -> None:
        """
        Record error occurrence.
        
        Args:
            error_type: Type of error
            component: Component where error occurred
        """
        if not self.metrics_enabled:
            return
        
        self.errors.labels(
            error_type=error_type,
            component=component
        ).inc()
    
    def record_security_scan(
        self,
        scan_type: str,
        vulnerabilities: Dict[str, int]
    ) -> None:
        """
        Record security scan results.
        
        Args:
            scan_type: Type of security scan
            vulnerabilities: Dict of severity -> count
        """
        if not self.metrics_enabled:
            return
        
        self.security_scans.labels(scan_type=scan_type).inc()
        
        for severity, count in vulnerabilities.items():
            self.vulnerabilities_found.labels(severity=severity).set(count)
    
    def update_system_metrics(self) -> None:
        """Update system resource metrics."""
        if not self.metrics_enabled:
            return
        
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=0.1)
        self.cpu_usage.set(cpu_percent)
        
        # Memory usage
        memory = psutil.virtual_memory()
        self.memory_usage.set(memory.used)
        self.memory_usage_percent.set(memory.percent)


class HealthCheck:
    """
    Health check system for production readiness.
    
    Provides:
    - Liveness probes (is service running?)
    - Readiness probes (is service ready to handle requests?)
    - Dependency checks
    """
    
    def __init__(self) -> None:
        """Initialize health check system."""
        self.checks: Dict[str, Callable[[], bool]] = {}
        self.last_check: Optional[HealthStatus] = None
    
    def register_check(self, name: str, check_func: Callable[[], bool]) -> None:
        """
        Register a health check.
        
        Args:
            name: Name of the check
            check_func: Function that returns True if healthy
        """
        self.checks[name] = check_func
    
    def check_system_resources(self) -> bool:
        """Check if system resources are adequate."""
        try:
            memory = psutil.virtual_memory()
            cpu = psutil.cpu_percent(interval=0.1)
            
            # Check thresholds
            memory_ok = memory.percent < 90
            cpu_ok = cpu < 90
            
            return memory_ok and cpu_ok
        except Exception:
            return False
    
    def check_dependencies(self) -> bool:
        """Check if critical dependencies are available."""
        try:
            # Check if quantum libraries are available
            import numpy
            import scipy
            return True
        except ImportError:
            return False
    
    def check_disk_space(self) -> bool:
        """Check if adequate disk space is available."""
        try:
            disk = psutil.disk_usage('/')
            return disk.percent < 90
        except Exception:
            return False
    
    def liveness_probe(self) -> HealthStatus:
        """
        Liveness probe - checks if service is alive.
        
        Returns:
            HealthStatus indicating if service is running
        """
        status = HealthStatus(
            healthy=True,
            status="healthy",
            timestamp=time.time()
        )
        
        status.checks["alive"] = True
        status.messages.append("Service is running")
        
        return status
    
    def readiness_probe(self) -> HealthStatus:
        """
        Readiness probe - checks if service is ready to handle requests.
        
        Returns:
            HealthStatus indicating if service is ready
        """
        status = HealthStatus(
            healthy=True,
            status="healthy",
            timestamp=time.time()
        )
        
        # Run all registered checks
        for name, check_func in self.checks.items():
            try:
                result = check_func()
                status.checks[name] = result
                
                if not result:
                    status.healthy = False
                    status.status = "degraded"
                    status.messages.append(f"Check failed: {name}")
            except Exception as e:
                status.checks[name] = False
                status.healthy = False
                status.status = "unhealthy"
                status.messages.append(f"Check error: {name}: {str(e)}")
        
        # Run default checks
        status.checks["system_resources"] = self.check_system_resources()
        status.checks["dependencies"] = self.check_dependencies()
        status.checks["disk_space"] = self.check_disk_space()
        
        # Update overall status
        if not all([
            status.checks["system_resources"],
            status.checks["dependencies"],
            status.checks["disk_space"]
        ]):
            status.healthy = False
            status.status = "degraded"
        
        self.last_check = status
        return status
    
    def get_health_json(self) -> str:
        """
        Get health status as JSON.
        
        Returns:
            JSON string of health status
        """
        if self.last_check is None:
            self.last_check = self.readiness_probe()
        
        return json.dumps({
            "healthy": self.last_check.healthy,
            "status": self.last_check.status,
            "timestamp": datetime.fromtimestamp(self.last_check.timestamp).isoformat(),
            "checks": self.last_check.checks,
            "messages": self.last_check.messages
        }, indent=2)


class MonitoringDashboard:
    """Simple monitoring dashboard for viewing metrics."""
    
    def __init__(self, metrics: PrometheusMetrics, health: HealthCheck) -> None:
        """
        Initialize monitoring dashboard.
        
        Args:
            metrics: Prometheus metrics instance
            health: Health check instance
        """
        self.metrics = metrics
        self.health = health
    
    def print_status(self) -> None:
        """Print current system status."""
        print("\n" + "=" * 70)
        print("HOUDINIS MONITORING DASHBOARD")
        print("=" * 70)
        
        # Health status
        health_status = self.health.readiness_probe()
        status_emoji = "" if health_status.healthy else ""
        print(f"\n{status_emoji} Health Status: {health_status.status.upper()}")
        
        print("\n Health Checks:")
        for check_name, result in health_status.checks.items():
            emoji = "" if result else ""
            print(f"  {emoji} {check_name}: {'OK' if result else 'FAILED'}")
        
        if health_status.messages:
            print("\n Messages:")
            for msg in health_status.messages:
                print(f"  - {msg}")
        
        # System metrics
        print("\n System Metrics:")
        memory = psutil.virtual_memory()
        cpu = psutil.cpu_percent(interval=0.1)
        disk = psutil.disk_usage('/')
        
        print(f"  CPU Usage: {cpu:.1f}%")
        print(f"  Memory: {memory.percent:.1f}% ({memory.used / 1024**3:.1f}GB / {memory.total / 1024**3:.1f}GB)")
        print(f"  Disk: {disk.percent:.1f}% ({disk.used / 1024**3:.1f}GB / {disk.total / 1024**3:.1f}GB)")
        
        print("\n" + "=" * 70)


def demonstrate_monitoring() -> None:
    """Demonstrate monitoring system."""
    print("=" * 70)
    print("HOUDINIS MONITORING SYSTEM DEMONSTRATION")
    print("=" * 70)
    
    # Initialize monitoring
    metrics = PrometheusMetrics(port=8000, enable_server=False)
    health = HealthCheck()
    dashboard = MonitoringDashboard(metrics, health)
    
    # Register custom health checks
    def check_quantum_backend() -> bool:
        """Check if quantum backend is available."""
        try:
            from quantum.simulator import QuantumSimulator
            sim = QuantumSimulator(num_qubits=2)
            return True
        except Exception:
            return False
    
    health.register_check("quantum_backend", check_quantum_backend)
    
    # Simulate some algorithm executions
    print("\n[*] Simulating algorithm executions...")
    
    for i in range(5):
        algorithm = ["shor", "grover", "deutsch_jozsa"][i % 3]
        backend = ["qiskit", "cirq", "simulator"][i % 3]
        duration = 1.5 + i * 0.5
        success = i % 4 != 0
        
        metrics.record_algorithm_execution(
            algorithm=algorithm,
            backend=backend,
            duration=duration,
            success=success,
            circuit_depth=50 + i * 10
        )
        
        print(f"  [{i+1}] {algorithm} on {backend}: {duration:.2f}s - {'' if success else ''}")
    
    # Update system metrics
    metrics.update_system_metrics()
    
    # Display dashboard
    dashboard.print_status()
    
    print(f"\n[+] Metrics server can be started on port {metrics.port}")
    print(f"[+] Access metrics at: http://localhost:{metrics.port}/metrics")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    demonstrate_monitoring()
