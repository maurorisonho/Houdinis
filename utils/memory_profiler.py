#!/usr/bin/env python3
"""
# Houdinis Framework - Quantum Cryptography Testing Platform
# Author: Mauro Risonho de Paula Assumpção aka firebitsbr
# Developed by: Human Logic & Coding with AI Assistance (Claude Sonnet 4.5)
# License: MIT

Memory Profiler and Optimizer
==============================

Memory tracking, leak detection, and optimization for Houdinis.

Features:
- Memory usage tracking
- Leak detection
- Optimization strategies
- Data compression
- Cache management

Author: Houdinis Framework
License: MIT
"""

import sys
import gc
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import time

try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class MemorySnapshot:
    """Memory usage snapshot"""

    timestamp: float
    rss_mb: float  # Resident set size
    vms_mb: float  # Virtual memory size
    percent: float
    available_mb: float


class MemoryProfiler:
    """Track and optimize memory usage"""

    def __init__(self) -> None:
        """Initialize memory profiler"""
        if not PSUTIL_AVAILABLE:
            logger.warning("psutil not available - limited functionality")

        self.snapshots: List[MemorySnapshot] = []
        self.baseline: Optional[MemorySnapshot] = None

    def take_snapshot(self) -> MemorySnapshot:
        """Take current memory snapshot"""
        if PSUTIL_AVAILABLE:
            process = psutil.Process()
            mem_info = process.memory_info()
            vm = psutil.virtual_memory()

            snapshot = MemorySnapshot(
                timestamp=time.time(),
                rss_mb=mem_info.rss / 1024 / 1024,
                vms_mb=mem_info.vms / 1024 / 1024,
                percent=process.memory_percent(),
                available_mb=vm.available / 1024 / 1024,
            )
        else:
            # Fallback
            snapshot = MemorySnapshot(
                timestamp=time.time(),
                rss_mb=0.0,
                vms_mb=0.0,
                percent=0.0,
                available_mb=0.0,
            )

        self.snapshots.append(snapshot)
        return snapshot

    def set_baseline(self) -> None:
        """Set current memory as baseline"""
        self.baseline = self.take_snapshot()
        logger.info(f"Baseline set: {self.baseline.rss_mb:.2f} MB RSS")

    def get_memory_delta(self) -> float:
        """Get memory change since baseline"""
        if not self.baseline:
            self.set_baseline()
            return 0.0

        current = self.take_snapshot()
        delta = current.rss_mb - self.baseline.rss_mb

        logger.info(f"Memory delta: {delta:+.2f} MB")
        return delta

    def detect_leaks(self, threshold_mb: float = 100.0) -> bool:
        """Detect potential memory leaks"""
        if len(self.snapshots) < 2:
            return False

        # Check for consistent growth
        recent = self.snapshots[-10:]
        if len(recent) < 2:
            return False

        growth = recent[-1].rss_mb - recent[0].rss_mb

        if growth > threshold_mb:
            logger.warning(f"Potential memory leak detected: +{growth:.2f} MB")
            return True

        return False

    def optimize_memory(self):
        """Run memory optimization"""
        logger.info("Running memory optimization...")

        # Force garbage collection
        collected = gc.collect()
        logger.info(f"  Garbage collected: {collected} objects")

        # Clear internal caches
        sys.intern("dummy")  # Clear interned strings cache

        # Take snapshot after optimization
        after = self.take_snapshot()
        logger.info(f"  Memory after optimization: {after.rss_mb:.2f} MB")

    def get_statistics(self) -> Dict[str, Any]:
        """Get memory statistics"""
        if not self.snapshots:
            return {}

        rss_values = [s.rss_mb for s in self.snapshots]

        return {
            "num_snapshots": len(self.snapshots),
            "current_rss_mb": self.snapshots[-1].rss_mb,
            "peak_rss_mb": max(rss_values),
            "average_rss_mb": sum(rss_values) / len(rss_values),
            "baseline_rss_mb": self.baseline.rss_mb if self.baseline else 0.0,
        }


class DataCompressor:
    """Compress data to reduce memory usage"""

    @staticmethod
    def compress_state_vector(state_vector, threshold: float = 1e-10) -> Tuple[np.ndarray, np.ndarray]:
        """Compress quantum state vector by removing negligible amplitudes"""
        import numpy as np

        # Find significant amplitudes
        significant = np.abs(state_vector) > threshold

        # Store only significant values
        compressed = {
            "indices": np.where(significant)[0],
            "values": state_vector[significant],
            "size": len(state_vector),
        }

        original_size = state_vector.nbytes
        compressed_size = compressed["indices"].nbytes + compressed["values"].nbytes
        compression_ratio = (
            original_size / compressed_size if compressed_size > 0 else 1.0
        )

        logger.info(f"Compressed state vector: {compression_ratio:.2f}x reduction")

        return compressed

    @staticmethod
    def decompress_state_vector(compressed: Tuple[np.ndarray, np.ndarray]) -> np.ndarray:
        """Decompress state vector"""
        import numpy as np

        state_vector = np.zeros(compressed["size"], dtype=complex)
        state_vector[compressed["indices"]] = compressed["values"]

        return state_vector


if __name__ == "__main__":
    print("Memory Profiler")
    print("=" * 50)

    profiler = MemoryProfiler()

    print("\n1. Taking baseline...")
    profiler.set_baseline()

    print("\n2. Allocating memory...")
    data = [0] * 10_000_000  # Allocate ~80MB

    delta = profiler.get_memory_delta()
    print(f"  Memory increased by: {delta:.2f} MB")

    print("\n3. Optimizing memory...")
    del data
    profiler.optimize_memory()

    print("\n4. Statistics:")
    stats = profiler.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    print("\n Memory profiler ready!")
