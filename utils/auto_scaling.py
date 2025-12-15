"""
Houdinis Framework - Auto-Scaling and Performance Optimization
Data de Criação: 15 de dezembro de 2025
Author: Mauro Risonho de Paula Assumpção aka firebitsbr
License: MIT

Automated scaling policies, caching strategies, and performance optimization.
"""

import time
import threading
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from collections import deque
import json

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


@dataclass
class ScalingMetrics:
    """Metrics for scaling decisions."""
    timestamp: float
    cpu_percent: float
    memory_percent: float
    request_count: int
    response_time_ms: float
    error_rate: float


@dataclass
class ScalingPolicy:
    """Auto-scaling policy configuration."""
    name: str
    metric_type: str  # cpu, memory, requests, latency
    scale_up_threshold: float
    scale_down_threshold: float
    min_instances: int
    max_instances: int
    cooldown_seconds: int = 300
    enabled: bool = True


class AutoScaler:
    """
    Automatic scaling manager for Houdinis services.
    
    Features:
    - CPU-based scaling
    - Memory-based scaling
    - Request-rate scaling
    - Latency-based scaling
    - Predictive scaling
    """
    
    def __init__(self, service_name: str = "houdinis") -> None:
        """
        Initialize auto-scaler.
        
        Args:
            service_name: Name of service to scale
        """
        self.service_name = service_name
        self.current_instances = 1
        self.policies: List[ScalingPolicy] = []
        self.metrics_history: deque = deque(maxlen=100)
        self.last_scale_time = 0
        self.scaling_events: List[Dict[str, Any]] = []
        
        # Initialize default policies
        self._initialize_default_policies()
    
    def _initialize_default_policies(self) -> None:
        """Initialize default scaling policies."""
        self.policies = [
            ScalingPolicy(
                name="cpu_scaling",
                metric_type="cpu",
                scale_up_threshold=70.0,
                scale_down_threshold=30.0,
                min_instances=1,
                max_instances=10,
                cooldown_seconds=300
            ),
            ScalingPolicy(
                name="memory_scaling",
                metric_type="memory",
                scale_up_threshold=80.0,
                scale_down_threshold=40.0,
                min_instances=1,
                max_instances=10,
                cooldown_seconds=300
            ),
            ScalingPolicy(
                name="request_scaling",
                metric_type="requests",
                scale_up_threshold=1000.0,
                scale_down_threshold=100.0,
                min_instances=1,
                max_instances=20,
                cooldown_seconds=180
            )
        ]
    
    def collect_metrics(self) -> ScalingMetrics:
        """
        Collect current system metrics.
        
        Returns:
            Current metrics
        """
        if PSUTIL_AVAILABLE:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_percent = psutil.virtual_memory().percent
        else:
            # Simulate metrics if psutil not available
            cpu_percent = 50.0
            memory_percent = 60.0
        
        metrics = ScalingMetrics(
            timestamp=time.time(),
            cpu_percent=cpu_percent,
            memory_percent=memory_percent,
            request_count=0,  # Would be from actual service metrics
            response_time_ms=0.0,
            error_rate=0.0
        )
        
        self.metrics_history.append(metrics)
        return metrics
    
    def evaluate_scaling_decision(self) -> Optional[str]:
        """
        Evaluate if scaling action is needed.
        
        Returns:
            'scale_up', 'scale_down', or None
        """
        if not self.metrics_history:
            return None
        
        # Check cooldown period
        if time.time() - self.last_scale_time < 60:
            return None
        
        current_metrics = self.metrics_history[-1]
        
        for policy in self.policies:
            if not policy.enabled:
                continue
            
            metric_value = self._get_metric_value(current_metrics, policy.metric_type)
            
            # Check scale up condition
            if metric_value > policy.scale_up_threshold:
                if self.current_instances < policy.max_instances:
                    return "scale_up"
            
            # Check scale down condition
            if metric_value < policy.scale_down_threshold:
                if self.current_instances > policy.min_instances:
                    return "scale_down"
        
        return None
    
    def _get_metric_value(self, metrics: ScalingMetrics, metric_type: str) -> float:
        """Get specific metric value."""
        if metric_type == "cpu":
            return metrics.cpu_percent
        elif metric_type == "memory":
            return metrics.memory_percent
        elif metric_type == "requests":
            return float(metrics.request_count)
        elif metric_type == "latency":
            return metrics.response_time_ms
        return 0.0
    
    def scale_up(self, count: int = 1) -> bool:
        """
        Scale up instances.
        
        Args:
            count: Number of instances to add
            
        Returns:
            Success status
        """
        print(f"\n[*] Scaling up {self.service_name}")
        print(f"    Current: {self.current_instances} instances")
        print(f"    Adding: {count} instances")
        
        new_count = self.current_instances + count
        
        # Check max instances
        max_allowed = max(p.max_instances for p in self.policies)
        if new_count > max_allowed:
            print(f"[!] Cannot exceed max instances: {max_allowed}")
            return False
        
        # Simulate instance creation
        time.sleep(0.3)
        
        self.current_instances = new_count
        self.last_scale_time = time.time()
        
        event = {
            "timestamp": datetime.now().isoformat(),
            "action": "scale_up",
            "from_instances": self.current_instances - count,
            "to_instances": self.current_instances,
            "reason": "Threshold exceeded"
        }
        self.scaling_events.append(event)
        
        print(f"[+] Scaled to {self.current_instances} instances")
        return True
    
    def scale_down(self, count: int = 1) -> bool:
        """
        Scale down instances.
        
        Args:
            count: Number of instances to remove
            
        Returns:
            Success status
        """
        print(f"\n[*] Scaling down {self.service_name}")
        print(f"    Current: {self.current_instances} instances")
        print(f"    Removing: {count} instances")
        
        new_count = self.current_instances - count
        
        # Check min instances
        min_allowed = min(p.min_instances for p in self.policies)
        if new_count < min_allowed:
            print(f"[!] Cannot go below min instances: {min_allowed}")
            return False
        
        # Simulate instance termination
        time.sleep(0.2)
        
        self.current_instances = new_count
        self.last_scale_time = time.time()
        
        event = {
            "timestamp": datetime.now().isoformat(),
            "action": "scale_down",
            "from_instances": self.current_instances + count,
            "to_instances": self.current_instances,
            "reason": "Below threshold"
        }
        self.scaling_events.append(event)
        
        print(f"[+] Scaled to {self.current_instances} instances")
        return True
    
    def get_scaling_stats(self) -> Dict[str, Any]:
        """Get scaling statistics."""
        return {
            "service": self.service_name,
            "current_instances": self.current_instances,
            "total_events": len(self.scaling_events),
            "scale_up_events": len([e for e in self.scaling_events if e["action"] == "scale_up"]),
            "scale_down_events": len([e for e in self.scaling_events if e["action"] == "scale_down"]),
            "policies_enabled": sum(1 for p in self.policies if p.enabled),
            "metrics_collected": len(self.metrics_history)
        }


class CacheManager:
    """
    Intelligent caching system for Houdinis.
    
    Features:
    - LRU cache eviction
    - TTL-based expiration
    - Cache statistics
    - Hit rate optimization
    """
    
    def __init__(self, max_size: int = 1000, default_ttl: int = 3600) -> None:
        """
        Initialize cache manager.
        
        Args:
            max_size: Maximum cache entries
            default_ttl: Default TTL in seconds
        """
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.access_order: deque = deque(maxlen=max_size)
        
        self.hits = 0
        self.misses = 0
        self.evictions = 0
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None
        """
        if key not in self.cache:
            self.misses += 1
            return None
        
        entry = self.cache[key]
        
        # Check TTL
        if time.time() - entry["timestamp"] > entry["ttl"]:
            del self.cache[key]
            self.misses += 1
            return None
        
        # Update access order (LRU)
        if key in self.access_order:
            self.access_order.remove(key)
        self.access_order.append(key)
        
        self.hits += 1
        return entry["value"]
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        Set cache value.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds
        """
        # Evict if at capacity
        if len(self.cache) >= self.max_size and key not in self.cache:
            self._evict_lru()
        
        self.cache[key] = {
            "value": value,
            "timestamp": time.time(),
            "ttl": ttl or self.default_ttl
        }
        
        if key in self.access_order:
            self.access_order.remove(key)
        self.access_order.append(key)
    
    def _evict_lru(self) -> None:
        """Evict least recently used entry."""
        if self.access_order:
            lru_key = self.access_order.popleft()
            if lru_key in self.cache:
                del self.cache[lru_key]
                self.evictions += 1
    
    def invalidate(self, key: str) -> bool:
        """
        Invalidate cache entry.
        
        Args:
            key: Cache key
            
        Returns:
            True if key was present
        """
        if key in self.cache:
            del self.cache[key]
            if key in self.access_order:
                self.access_order.remove(key)
            return True
        return False
    
    def clear(self) -> None:
        """Clear all cache entries."""
        self.cache.clear()
        self.access_order.clear()
    
    def get_hit_rate(self) -> float:
        """
        Calculate cache hit rate.
        
        Returns:
            Hit rate as percentage
        """
        total = self.hits + self.misses
        if total == 0:
            return 0.0
        return (self.hits / total) * 100
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "hits": self.hits,
            "misses": self.misses,
            "evictions": self.evictions,
            "hit_rate": self.get_hit_rate(),
            "memory_usage_mb": self._estimate_size_mb()
        }
    
    def _estimate_size_mb(self) -> float:
        """Estimate cache memory usage."""
        # Simplified estimation
        return len(self.cache) * 0.001  # Rough estimate


def demonstrate_auto_scaling() -> None:
    """Demonstrate auto-scaling capabilities."""
    print("=" * 70)
    print("HOUDINIS AUTO-SCALING DEMONSTRATION")
    print("=" * 70)
    
    scaler = AutoScaler("houdinis-api")
    
    print(f"\n[*] Initial state: {scaler.current_instances} instance(s)")
    
    # Simulate load increase
    print("\n[*] Simulating high load scenario...")
    for i in range(3):
        metrics = scaler.collect_metrics()
        print(f"    CPU: {metrics.cpu_percent:.1f}%, Memory: {metrics.memory_percent:.1f}%")
        
        decision = scaler.evaluate_scaling_decision()
        if decision == "scale_up":
            scaler.scale_up()
            break
        time.sleep(0.5)
    
    # Show stats
    stats = scaler.get_scaling_stats()
    print(f"\n[*] Scaling Statistics:")
    print(f"    Current Instances: {stats['current_instances']}")
    print(f"    Scale Up Events: {stats['scale_up_events']}")
    print(f"    Total Events: {stats['total_events']}")
    
    # Cache demonstration
    print("\n" + "=" * 70)
    print("CACHING DEMONSTRATION")
    print("=" * 70)
    
    cache = CacheManager(max_size=100, default_ttl=3600)
    
    # Store some values
    print("\n[*] Storing values in cache...")
    cache.set("user:123", {"name": "Alice", "role": "admin"})
    cache.set("session:abc", {"token": "xyz", "expires": 3600})
    cache.set("config:app", {"debug": False, "version": "1.0"})
    
    # Retrieve values
    print("[*] Retrieving values...")
    user = cache.get("user:123")
    print(f"    Retrieved user: {user}")
    
    session = cache.get("session:abc")
    print(f"    Retrieved session: {session}")
    
    # Try non-existent key
    missing = cache.get("user:999")
    print(f"    Missing key: {missing}")
    
    # Show cache stats
    stats = cache.get_stats()
    print(f"\n[*] Cache Statistics:")
    print(f"    Size: {stats['size']}/{stats['max_size']}")
    print(f"    Hits: {stats['hits']}")
    print(f"    Misses: {stats['misses']}")
    print(f"    Hit Rate: {stats['hit_rate']:.1f}%")
    
    print("\n" + "=" * 70)
    print("[+] Performance optimization demonstration complete")
    print("=" * 70)


if __name__ == "__main__":
    demonstrate_auto_scaling()
