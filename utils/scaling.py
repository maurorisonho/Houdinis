#!/usr/bin/env python3
"""
Horizontal Scaling Infrastructure
==================================

Load balancing, worker pools, task queuing, and auto-scaling.

Features:
- Worker pool management
- Task queue system
- Load balancing
- Auto-scaling
- Health monitoring

Author: Houdinis Framework
License: MIT
"""

import time
import logging
import threading
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass
from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WorkerState(Enum):
    """Worker state enumeration"""
    IDLE = "idle"
    BUSY = "busy"
    STOPPED = "stopped"


@dataclass
class Worker:
    """Worker process information"""
    worker_id: int
    state: WorkerState
    tasks_completed: int = 0
    last_active: float = 0.0
    
    def is_idle(self) -> bool:
        """Check if worker is idle"""
        return self.state == WorkerState.IDLE


class WorkerPool:
    """Manage pool of workers"""
    
    def __init__(self, initial_size: int = 4, max_size: int = 16):
        """
        Initialize worker pool.
        
        Args:
            initial_size: Initial number of workers
            max_size: Maximum number of workers
        """
        self.initial_size = initial_size
        self.max_size = max_size
        self.workers: List[Worker] = []
        self.executor = ThreadPoolExecutor(max_workers=max_size)
        self.task_queue: Queue = Queue()
        self.running = False
        
        self._initialize_workers(initial_size)
        logger.info(f"Worker pool initialized: {initial_size}/{max_size} workers")
    
    def _initialize_workers(self, count: int):
        """Initialize workers"""
        for i in range(count):
            worker = Worker(
                worker_id=i,
                state=WorkerState.IDLE,
                last_active=time.time()
            )
            self.workers.append(worker)
    
    def scale_up(self, count: int = 1):
        """Add more workers"""
        current_size = len(self.workers)
        new_size = min(current_size + count, self.max_size)
        
        for i in range(current_size, new_size):
            worker = Worker(
                worker_id=i,
                state=WorkerState.IDLE,
                last_active=time.time()
            )
            self.workers.append(worker)
        
        added = new_size - current_size
        if added > 0:
            logger.info(f"Scaled up: +{added} workers ({new_size} total)")
        
        return added
    
    def scale_down(self, count: int = 1):
        """Remove idle workers"""
        idle_workers = [w for w in self.workers if w.is_idle()]
        
        to_remove = min(count, len(idle_workers))
        to_remove = min(to_remove, len(self.workers) - self.initial_size)
        
        if to_remove > 0:
            for _ in range(to_remove):
                worker = idle_workers.pop()
                worker.state = WorkerState.STOPPED
                self.workers.remove(worker)
            
            logger.info(f"Scaled down: -{to_remove} workers ({len(self.workers)} remaining)")
        
        return to_remove
    
    def submit_task(self, func: Callable, *args, **kwargs):
        """Submit task to queue"""
        self.task_queue.put((func, args, kwargs))
    
    def get_idle_worker(self) -> Optional[Worker]:
        """Get next idle worker"""
        for worker in self.workers:
            if worker.is_idle():
                return worker
        return None
    
    def get_stats(self) -> Dict[str, Any]:
        """Get worker pool statistics"""
        idle = sum(1 for w in self.workers if w.state == WorkerState.IDLE)
        busy = sum(1 for w in self.workers if w.state == WorkerState.BUSY)
        
        return {
            'total_workers': len(self.workers),
            'idle_workers': idle,
            'busy_workers': busy,
            'queue_size': self.task_queue.qsize(),
            'total_tasks_completed': sum(w.tasks_completed for w in self.workers)
        }


class AutoScaler:
    """Automatic scaling based on load"""
    
    def __init__(
        self,
        worker_pool: WorkerPool,
        scale_up_threshold: float = 0.8,
        scale_down_threshold: float = 0.2,
        check_interval: float = 10.0
    ):
        """
        Initialize auto-scaler.
        
        Args:
            worker_pool: Worker pool to manage
            scale_up_threshold: Utilization threshold to scale up
            scale_down_threshold: Utilization threshold to scale down
            check_interval: Check interval in seconds
        """
        self.worker_pool = worker_pool
        self.scale_up_threshold = scale_up_threshold
        self.scale_down_threshold = scale_down_threshold
        self.check_interval = check_interval
        self.running = False
        self.monitor_thread: Optional[threading.Thread] = None
    
    def start(self):
        """Start auto-scaling"""
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        logger.info("Auto-scaler started")
    
    def stop(self):
        """Stop auto-scaling"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5.0)
        logger.info("Auto-scaler stopped")
    
    def _monitor_loop(self):
        """Monitoring loop for auto-scaling"""
        while self.running:
            try:
                self._check_and_scale()
                time.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"Auto-scaler error: {e}")
    
    def _check_and_scale(self):
        """Check load and scale if needed"""
        stats = self.worker_pool.get_stats()
        
        if stats['total_workers'] == 0:
            return
        
        utilization = stats['busy_workers'] / stats['total_workers']
        
        if utilization > self.scale_up_threshold:
            self.worker_pool.scale_up(2)
            logger.info(f"Auto-scaled up (utilization: {utilization:.2%})")
        
        elif utilization < self.scale_down_threshold:
            self.worker_pool.scale_down(1)
            logger.info(f"Auto-scaled down (utilization: {utilization:.2%})")


class LoadBalancer:
    """Balance load across workers"""
    
    def __init__(self, strategy: str = "round_robin"):
        """
        Initialize load balancer.
        
        Args:
            strategy: Load balancing strategy
        """
        self.strategy = strategy
        self.current_index = 0
    
    def select_worker(self, workers: List[Worker]) -> Optional[Worker]:
        """Select worker based on strategy"""
        idle_workers = [w for w in workers if w.is_idle()]
        
        if not idle_workers:
            return None
        
        if self.strategy == "round_robin":
            worker = idle_workers[self.current_index % len(idle_workers)]
            self.current_index += 1
            return worker
        
        elif self.strategy == "least_loaded":
            return min(idle_workers, key=lambda w: w.tasks_completed)
        
        return idle_workers[0]


if __name__ == '__main__':
    print("Horizontal Scaling Infrastructure")
    print("=" * 50)
    
    # Test worker pool
    print("\n1. Creating worker pool...")
    pool = WorkerPool(initial_size=2, max_size=8)
    
    print("\n2. Scaling up...")
    pool.scale_up(2)
    
    stats = pool.get_stats()
    print(f"  Total workers: {stats['total_workers']}")
    print(f"  Idle workers: {stats['idle_workers']}")
    
    print("\n3. Testing auto-scaler...")
    scaler = AutoScaler(pool, check_interval=1.0)
    scaler.start()
    
    time.sleep(2)
    scaler.stop()
    
    print("\n4. Testing load balancer...")
    balancer = LoadBalancer(strategy="round_robin")
    
    for i in range(3):
        worker = balancer.select_worker(pool.workers)
        if worker:
            print(f"  Selected worker: {worker.worker_id}")
    
    print("\n Scaling infrastructure ready!")
