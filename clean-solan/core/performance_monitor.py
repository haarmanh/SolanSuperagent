"""
Performance Monitoring Utilities (Optimized)
"""

import time
import functools
from typing import Dict, List
from collections import defaultdict, deque

class PerformanceMonitor:
    """Monitor API performance metrics"""

    def __init__(self, max_history: int = 1000):
        self.metrics: Dict[str, deque] = defaultdict(lambda: deque(maxlen=max_history))
        self.counters: Dict[str, int] = defaultdict(int)

    def record_timing(self, endpoint: str, duration_ms: float):
        """Record timing for an endpoint"""
        self.metrics[f"{endpoint}_timing"].append(duration_ms)
        self.counters[f"{endpoint}_calls"] += 1

    def record_error(self, endpoint: str):
        """Record error for an endpoint"""
        self.counters[f"{endpoint}_errors"] += 1

    def get_stats(self, endpoint: str = None) -> Dict:
        """Get performance statistics"""
        if endpoint:
            timings = list(self.metrics.get(f"{endpoint}_timing", []))
            if timings:
                return {
                    "endpoint": endpoint,
                    "avg_ms": sum(timings) / len(timings),
                    "min_ms": min(timings),
                    "max_ms": max(timings),
                    "total_calls": self.counters.get(f"{endpoint}_calls", 0),
                    "total_errors": self.counters.get(f"{endpoint}_errors", 0)
                }
            return {"endpoint": endpoint, "no_data": True}

        stats = {}
        endpoints = set()
        for key in self.metrics.keys():
            if key.endswith('_timing'):
                endpoints.add(key[:-7])

        for ep in endpoints:
            stats[ep] = self.get_stats(ep)

        return stats

# Global monitor instance
performance_monitor = PerformanceMonitor()

def monitor_performance(func):
    """Decorator to monitor function performance"""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        endpoint = func.__name__

        try:
            result = await func(*args, **kwargs)
            duration_ms = (time.time() - start_time) * 1000
            performance_monitor.record_timing(endpoint, duration_ms)
            return result
        except Exception:
            performance_monitor.record_error(endpoint)
            raise

    return wrapper


