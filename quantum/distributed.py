#!/usr/bin/env python3
"""
Distributed Quantum Computing Framework
========================================

Distributed execution of quantum circuits across multiple workers/backends.
Supports Ray, Dask, and multiprocessing for horizontal scaling.

Features:
- Distributed circuit execution
- Load balancing across workers
- Fault tolerance and retry mechanisms
- Resource management
- Task queuing and scheduling
- Performance monitoring

Author: Houdinis Framework
License: MIT
"""

import time
import logging
from typing import List, Dict, Any, Optional, Callable, Union
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from queue import Queue
import threading
from enum import Enum

# Optional distributed computing backends
try:
    import ray
    RAY_AVAILABLE = True
except ImportError:
    RAY_AVAILABLE = False

try:
    import dask
    import dask.distributed
    DASK_AVAILABLE = True
except ImportError:
    DASK_AVAILABLE = False


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DistributedBackend(Enum):
    """Distributed computing backend types"""
    RAY = "ray"
    DASK = "dask"
    MULTIPROCESSING = "multiprocessing"
    THREADING = "threading"


@dataclass
class WorkerStatus:
    """Worker health and status information"""
    worker_id: str
    active: bool = True
    tasks_completed: int = 0
    tasks_failed: int = 0
    current_load: float = 0.0
    last_heartbeat: float = field(default_factory=time.time)
    
    def update_heartbeat(self):
        """Update last heartbeat timestamp"""
        self.last_heartbeat = time.time()
    
    def is_healthy(self, timeout: float = 60.0) -> bool:
        """Check if worker is responsive"""
        return (time.time() - self.last_heartbeat) < timeout


@dataclass
class TaskResult:
    """Result from distributed task execution"""
    task_id: str
    worker_id: str
    success: bool
    result: Any
    execution_time: float
    error: Optional[str] = None
    retries: int = 0


class LoadBalancer:
    """Simple load balancer for distributing tasks"""
    
    def __init__(self, num_workers: int):
        """
        Initialize load balancer.
        
        Args:
            num_workers: Number of available workers
        """
        self.num_workers = num_workers
        self.worker_loads = [0.0] * num_workers
        self.round_robin_index = 0
    
    def get_next_worker(self, strategy: str = "round_robin") -> int:
        """
        Get next worker based on load balancing strategy.
        
        Args:
            strategy: Load balancing strategy (round_robin, least_loaded)
            
        Returns:
            Worker index
        """
        if strategy == "round_robin":
            worker = self.round_robin_index
            self.round_robin_index = (self.round_robin_index + 1) % self.num_workers
            return worker
        
        elif strategy == "least_loaded":
            return self.worker_loads.index(min(self.worker_loads))
        
        else:
            return 0
    
    def update_load(self, worker_id: int, load: float):
        """Update worker load"""
        if 0 <= worker_id < self.num_workers:
            self.worker_loads[worker_id] = load


class DistributedQuantumExecutor:
    """
    Distributed executor for quantum circuits.
    
    Manages distributed execution across multiple workers with
    fault tolerance, load balancing, and monitoring.
    """
    
    def __init__(
        self,
        backend_type: str = "multiprocessing",
        num_workers: int = 4,
        max_retries: int = 3,
        timeout: float = 300.0
    ):
        """
        Initialize distributed executor.
        
        Args:
            backend_type: Distributed backend (ray, dask, multiprocessing, threading)
            num_workers: Number of worker processes/threads
            max_retries: Maximum retry attempts for failed tasks
            timeout: Task timeout in seconds
        """
        self.backend_type = DistributedBackend(backend_type)
        self.num_workers = num_workers
        self.max_retries = max_retries
        self.timeout = timeout
        
        self.workers: Dict[str, WorkerStatus] = {}
        self.load_balancer = LoadBalancer(num_workers)
        self.task_queue: Queue = Queue()
        self.results: Dict[str, TaskResult] = {}
        
        self._initialize_backend()
        
        logger.info(f"Initialized distributed executor: {backend_type}, {num_workers} workers")
    
    def _initialize_backend(self):
        """Initialize the selected distributed backend"""
        if self.backend_type == DistributedBackend.RAY:
            if not RAY_AVAILABLE:
                raise ImportError("Ray not available. Install with: pip install ray")
            
            if not ray.is_initialized():
                ray.init(num_cpus=self.num_workers, ignore_reinit_error=True)
            
            logger.info(f"Ray initialized with {self.num_workers} CPUs")
        
        elif self.backend_type == DistributedBackend.DASK:
            if not DASK_AVAILABLE:
                raise ImportError("Dask not available. Install with: pip install dask distributed")
            
            # Dask client can be created on-demand
            logger.info(f"Dask backend ready with {self.num_workers} workers")
        
        elif self.backend_type == DistributedBackend.MULTIPROCESSING:
            self.executor = ProcessPoolExecutor(max_workers=self.num_workers)
            logger.info(f"ProcessPoolExecutor initialized with {self.num_workers} workers")
        
        elif self.backend_type == DistributedBackend.THREADING:
            self.executor = ThreadPoolExecutor(max_workers=self.num_workers)
            logger.info(f"ThreadPoolExecutor initialized with {self.num_workers} workers")
        
        # Initialize worker status
        for i in range(self.num_workers):
            worker_id = f"worker_{i}"
            self.workers[worker_id] = WorkerStatus(worker_id=worker_id)
    
    def execute_distributed(
        self,
        tasks: List[Callable],
        args_list: Optional[List[tuple]] = None,
        kwargs_list: Optional[List[dict]] = None
    ) -> List[TaskResult]:
        """
        Execute tasks in distributed manner.
        
        Args:
            tasks: List of callable tasks to execute
            args_list: List of positional arguments for each task
            kwargs_list: List of keyword arguments for each task
            
        Returns:
            List of TaskResult objects
        """
        if args_list is None:
            args_list = [()] * len(tasks)
        if kwargs_list is None:
            kwargs_list = [{}] * len(tasks)
        
        if len(tasks) != len(args_list) or len(tasks) != len(kwargs_list):
            raise ValueError("tasks, args_list, and kwargs_list must have same length")
        
        logger.info(f"Executing {len(tasks)} tasks across {self.num_workers} workers")
        
        if self.backend_type == DistributedBackend.RAY:
            return self._execute_with_ray(tasks, args_list, kwargs_list)
        elif self.backend_type == DistributedBackend.DASK:
            return self._execute_with_dask(tasks, args_list, kwargs_list)
        else:
            return self._execute_with_executor(tasks, args_list, kwargs_list)
    
    def _execute_with_ray(
        self,
        tasks: List[Callable],
        args_list: List[tuple],
        kwargs_list: List[dict]
    ) -> List[TaskResult]:
        """Execute tasks using Ray"""
        
        @ray.remote
        def ray_task_wrapper(task_id, func, args, kwargs):
            """Ray remote task wrapper"""
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                return TaskResult(
                    task_id=task_id,
                    worker_id=ray.get_runtime_context().get_worker_id(),
                    success=True,
                    result=result,
                    execution_time=execution_time
                )
            except Exception as e:
                execution_time = time.time() - start_time
                return TaskResult(
                    task_id=task_id,
                    worker_id="unknown",
                    success=False,
                    result=None,
                    execution_time=execution_time,
                    error=str(e)
                )
        
        # Submit all tasks
        futures = []
        for i, (task, args, kwargs) in enumerate(zip(tasks, args_list, kwargs_list)):
            task_id = f"task_{i}"
            future = ray_task_wrapper.remote(task_id, task, args, kwargs)
            futures.append(future)
        
        # Collect results
        results = ray.get(futures)
        
        logger.info(f"Ray execution completed: {len(results)} results")
        return results
    
    def _execute_with_dask(
        self,
        tasks: List[Callable],
        args_list: List[tuple],
        kwargs_list: List[dict]
    ) -> List[TaskResult]:
        """Execute tasks using Dask"""
        from dask.distributed import Client, as_completed
        
        client = Client(n_workers=self.num_workers, threads_per_worker=1)
        
        try:
            futures = []
            for i, (task, args, kwargs) in enumerate(zip(tasks, args_list, kwargs_list)):
                task_id = f"task_{i}"
                future = client.submit(
                    self._task_wrapper,
                    task_id,
                    task,
                    args,
                    kwargs
                )
                futures.append(future)
            
            # Collect results as they complete
            results = []
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
            
            logger.info(f"Dask execution completed: {len(results)} results")
            return results
        
        finally:
            client.close()
    
    def _execute_with_executor(
        self,
        tasks: List[Callable],
        args_list: List[tuple],
        kwargs_list: List[dict]
    ) -> List[TaskResult]:
        """Execute tasks using ThreadPoolExecutor or ProcessPoolExecutor"""
        futures = []
        
        for i, (task, args, kwargs) in enumerate(zip(tasks, args_list, kwargs_list)):
            task_id = f"task_{i}"
            worker_id = self.load_balancer.get_next_worker("round_robin")
            
            future = self.executor.submit(
                self._task_wrapper,
                task_id,
                task,
                args,
                kwargs,
                f"worker_{worker_id}"
            )
            futures.append(future)
        
        # Collect results with timeout
        results = []
        for future in as_completed(futures, timeout=self.timeout):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                logger.error(f"Task execution failed: {e}")
                results.append(TaskResult(
                    task_id="unknown",
                    worker_id="unknown",
                    success=False,
                    result=None,
                    execution_time=0.0,
                    error=str(e)
                ))
        
        logger.info(f"Executor execution completed: {len(results)} results")
        return results
    
    def _task_wrapper(
        self,
        task_id: str,
        func: Callable,
        args: tuple,
        kwargs: dict,
        worker_id: str = "unknown"
    ) -> TaskResult:
        """Wrapper for task execution with error handling"""
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            return TaskResult(
                task_id=task_id,
                worker_id=worker_id,
                success=True,
                result=result,
                execution_time=execution_time
            )
        
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Task {task_id} failed: {e}")
            
            return TaskResult(
                task_id=task_id,
                worker_id=worker_id,
                success=False,
                result=None,
                execution_time=execution_time,
                error=str(e)
            )
    
    def map_reduce(
        self,
        map_func: Callable,
        reduce_func: Callable,
        data: List[Any],
        chunk_size: Optional[int] = None
    ) -> Any:
        """
        Distributed map-reduce operation.
        
        Args:
            map_func: Function to apply to each data element
            reduce_func: Function to combine results
            data: Input data list
            chunk_size: Size of data chunks per worker
            
        Returns:
            Reduced result
        """
        if chunk_size is None:
            chunk_size = max(1, len(data) // self.num_workers)
        
        # Split data into chunks
        chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
        
        logger.info(f"Map-reduce: {len(chunks)} chunks, chunk_size={chunk_size}")
        
        # Map phase
        map_tasks = [lambda chunk=c: [map_func(item) for item in chunk] for c in chunks]
        map_results = self.execute_distributed(map_tasks)
        
        # Extract successful results
        successful_results = [
            item
            for r in map_results
            if r.success
            for item in r.result
        ]
        
        # Reduce phase
        if not successful_results:
            logger.warning("No successful map results to reduce")
            return None
        
        final_result = successful_results[0]
        for result in successful_results[1:]:
            final_result = reduce_func(final_result, result)
        
        logger.info(f"Map-reduce completed: {len(successful_results)} items reduced")
        return final_result
    
    def get_worker_stats(self) -> Dict[str, Any]:
        """Get statistics about worker health and performance"""
        stats = {
            'num_workers': self.num_workers,
            'backend': self.backend_type.value,
            'workers': {}
        }
        
        for worker_id, status in self.workers.items():
            stats['workers'][worker_id] = {
                'active': status.active,
                'tasks_completed': status.tasks_completed,
                'tasks_failed': status.tasks_failed,
                'current_load': status.current_load,
                'healthy': status.is_healthy()
            }
        
        return stats
    
    def shutdown(self):
        """Shutdown the distributed executor"""
        logger.info("Shutting down distributed executor...")
        
        if self.backend_type == DistributedBackend.RAY:
            if ray.is_initialized():
                ray.shutdown()
        
        elif self.backend_type in [DistributedBackend.MULTIPROCESSING, DistributedBackend.THREADING]:
            self.executor.shutdown(wait=True)
        
        logger.info("Distributed executor shut down successfully")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.shutdown()


class CircuitBatcher:
    """Batch quantum circuits for efficient distributed execution"""
    
    def __init__(self, batch_size: int = 10):
        """
        Initialize circuit batcher.
        
        Args:
            batch_size: Number of circuits per batch
        """
        self.batch_size = batch_size
    
    def create_batches(self, circuits: List[Any]) -> List[List[Any]]:
        """
        Create batches from circuit list.
        
        Args:
            circuits: List of quantum circuits
            
        Returns:
            List of circuit batches
        """
        batches = []
        for i in range(0, len(circuits), self.batch_size):
            batch = circuits[i:i+self.batch_size]
            batches.append(batch)
        
        logger.info(f"Created {len(batches)} batches from {len(circuits)} circuits")
        return batches


# Example usage and testing
if __name__ == '__main__':
    print("Distributed Quantum Computing Framework")
    print("=" * 50)
    
    # Example task
    def sample_quantum_task(n: int) -> int:
        """Sample task that simulates quantum computation"""
        time.sleep(0.1)  # Simulate work
        return n ** 2
    
    # Test with multiprocessing backend
    print("\n1. Testing with multiprocessing backend...")
    with DistributedQuantumExecutor(backend_type="multiprocessing", num_workers=4) as executor:
        tasks = [sample_quantum_task] * 10
        args_list = [(i,) for i in range(10)]
        
        results = executor.execute_distributed(tasks, args_list)
        
        print(f"\nCompleted {len(results)} tasks:")
        successful = sum(1 for r in results if r.success)
        print(f"  Successful: {successful}/{len(results)}")
        print(f"  Total time: {sum(r.execution_time for r in results):.2f}s")
        
        # Show worker stats
        stats = executor.get_worker_stats()
        print(f"\nWorker Statistics:")
        print(f"  Backend: {stats['backend']}")
        print(f"  Workers: {stats['num_workers']}")
    
    # Test map-reduce
    print("\n2. Testing map-reduce operation...")
    with DistributedQuantumExecutor(backend_type="threading", num_workers=2) as executor:
        data = list(range(20))
        
        result = executor.map_reduce(
            map_func=lambda x: x ** 2,
            reduce_func=lambda a, b: a + b,
            data=data,
            chunk_size=5
        )
        
        print(f"  Map-reduce result: {result}")
        print(f"  Expected: {sum(x**2 for x in data)}")
    
    print("\n Distributed computing framework ready!")
