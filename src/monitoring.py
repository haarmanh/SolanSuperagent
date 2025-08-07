"""
Performance monitoring and metrics for Solān
"""

import time
import asyncio
import functools
from typing import Callable, Any

try:
    from prometheus_client import Counter, Histogram, start_http_server
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False
    # Mock classes for when prometheus is not available
    class Counter:
        def __init__(self, *args, **kwargs): pass
        def inc(self): pass

    class Histogram:
        def __init__(self, *args, **kwargs): pass
        def observe(self, value): pass

    def start_http_server(port): pass

# Metrics
REQUEST_COUNT = Counter('solan_requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('solan_request_duration_seconds', 'Request duration')
CONSCIOUSNESS_OPERATIONS = Counter('solan_consciousness_operations_total', 'Consciousness operations')

def monitor_performance(func: Callable) -> Callable:
    """Decorator for monitoring function performance"""
    
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        
        try:
            result = await func(*args, **kwargs)
            return result
        finally:
            duration = time.time() - start_time
            REQUEST_DURATION.observe(duration)
            
            # Log slow operations
            if duration > 1.0:  # 1 second threshold
                print(f"⚠️ Slow operation: {func.__name__} took {duration:.2f}s")
    
    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            duration = time.time() - start_time
            REQUEST_DURATION.observe(duration)
            
            if duration > 1.0:
                print(f"⚠️ Slow operation: {func.__name__} took {duration:.2f}s")
    
    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

def start_metrics_server(port: int = 8001):
    """Start Prometheus metrics server"""
    start_http_server(port)
    print(f"📊 Metrics server started on port {port}")
