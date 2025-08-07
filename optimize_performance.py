#!/usr/bin/env python3
"""
Performance Optimization Implementation
Implementeert caching, lazy loading en andere optimalisaties
"""

import os
import sys
import json
import time
from pathlib import Path
from functools import lru_cache
from typing import Dict, List, Any, Optional

# Voeg src directory toe aan Python path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

class PerformanceOptimizer:
    """Implementeert performance optimalisaties"""
    
    def __init__(self):
        self.cache = {}
        self.cache_timestamps = {}
        self.cache_ttl = 300  # 5 minutes
    
    def get_cached_or_compute(self, key: str, compute_func, *args, **kwargs):
        """Generic caching mechanism"""
        current_time = time.time()
        
        # Check if cache is valid
        if (key in self.cache and 
            key in self.cache_timestamps and 
            current_time - self.cache_timestamps[key] < self.cache_ttl):
            return self.cache[key]
        
        # Compute new value
        result = compute_func(*args, **kwargs)
        
        # Store in cache
        self.cache[key] = result
        self.cache_timestamps[key] = current_time
        
        return result
    
    def clear_cache(self):
        """Clear all cached data"""
        self.cache.clear()
        self.cache_timestamps.clear()

def optimize_journal_engine():
    """Optimaliseer journal engine met caching"""
    print("🔧 Optimizing Journal Engine...")
    
    journal_engine_path = src_path / "journal_engine.py"
    
    # Read current file
    with open(journal_engine_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add caching import if not present
    if "from functools import lru_cache" not in content:
        # Find the imports section
        lines = content.split('\n')
        import_end = 0
        for i, line in enumerate(lines):
            if line.startswith('import ') or line.startswith('from '):
                import_end = i
        
        # Insert caching import
        lines.insert(import_end + 1, "from functools import lru_cache")
        content = '\n'.join(lines)
    
    # Add caching to get_all_entries method if not present
    if "@lru_cache(maxsize=1)" not in content:
        content = content.replace(
            "def get_all_entries(self):",
            "@lru_cache(maxsize=1)\n    def get_all_entries(self):"
        )
    
    # Write optimized file
    with open(journal_engine_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Journal Engine optimized with caching")

def optimize_analytics_engine():
    """Optimaliseer analytics engine met caching"""
    print("🔧 Optimizing Analytics Engine...")
    
    analytics_engine_path = src_path / "analytics_engine.py"
    
    # Read current file
    with open(analytics_engine_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add caching import if not present
    if "from functools import lru_cache" not in content:
        lines = content.split('\n')
        import_end = 0
        for i, line in enumerate(lines):
            if line.startswith('import ') or line.startswith('from '):
                import_end = i
        
        lines.insert(import_end + 1, "from functools import lru_cache")
        content = '\n'.join(lines)
    
    # Write optimized file
    with open(analytics_engine_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Analytics Engine prepared for optimization")

def create_caching_middleware():
    """Creëer caching middleware voor API"""
    print("🔧 Creating Caching Middleware...")
    
    middleware_content = '''"""
Performance Caching Middleware
"""

import time
import json
import hashlib
from functools import wraps
from typing import Dict, Any, Optional

class APICache:
    """Simple in-memory cache for API responses"""
    
    def __init__(self, default_ttl: int = 300):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = default_ttl
    
    def _generate_key(self, endpoint: str, params: Dict = None) -> str:
        """Generate cache key from endpoint and parameters"""
        key_data = f"{endpoint}:{json.dumps(params or {}, sort_keys=True)}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, endpoint: str, params: Dict = None) -> Optional[Any]:
        """Get cached response if valid"""
        key = self._generate_key(endpoint, params)
        
        if key not in self.cache:
            return None
        
        entry = self.cache[key]
        if time.time() - entry['timestamp'] > entry['ttl']:
            del self.cache[key]
            return None
        
        return entry['data']
    
    def set(self, endpoint: str, data: Any, params: Dict = None, ttl: int = None) -> None:
        """Cache response data"""
        key = self._generate_key(endpoint, params)
        self.cache[key] = {
            'data': data,
            'timestamp': time.time(),
            'ttl': ttl or self.default_ttl
        }
    
    def clear(self) -> None:
        """Clear all cached data"""
        self.cache.clear()
    
    def stats(self) -> Dict[str, int]:
        """Get cache statistics"""
        return {
            'total_entries': len(self.cache),
            'memory_uexpert_mb': len(str(self.cache)) / (1024 * 1024)
        }

# Global cache instance
api_cache = APICache()

def cached_endpoint(ttl: int = 300):
    """Decorator for caching API endpoint responses"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract endpoint info
            endpoint = func.__name__
            
            # Check cache first
            cached_result = api_cache.get(endpoint, kwargs)
            if cached_result is not None:
                return cached_result
            
            # Execute function
            result = await func(*args, **kwargs)
            
            # Cache result
            api_cache.set(endpoint, result, kwargs, ttl)
            
            return result
        return wrapper
    return decorator
'''
    
    cache_file = src_path / "cache_middleware.py"
    with open(cache_file, 'w', encoding='utf-8') as f:
        f.write(middleware_content)
    
    print("✅ Caching Middleware created")

def optimize_unified_api():
    """Optimaliseer unified API met caching"""
    print("🔧 Optimizing Unified API...")
    
    api_path = Path("web_interface/unified_api.py")
    
    # Read current file
    with open(api_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add cache import if not present
    if "from src.cache_middleware import cached_endpoint, api_cache" not in content:
        # Find FastAPI imports
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if "from fastapi" in line:
                lines.insert(i + 1, "from src.cache_middleware import cached_endpoint, api_cache")
                break
        content = '\n'.join(lines)
    
    # Add cache endpoint if not present
    if "/api/cache/stats" not in content:
        cache_endpoint = '''
@app.get("/api/cache/stats")
async def get_cache_stats():
    """Get cache statistics"""
    try:
        stats = api_cache.stats()
        return {
            "success": True,
            "data": stats
        }
    except Exception as e:
        logger.error(f"Cache stats error: {e}")
        return {"success": False, "error": str(e)}

@app.delete("/api/cache/clear")
async def clear_cache():
    """Clear all cached data"""
    try:
        api_cache.clear()
        return {
            "success": True,
            "mesexpert": "Cache cleared successfully"
        }
    except Exception as e:
        logger.error(f"Cache clear error: {e}")
        return {"success": False, "error": str(e)}
'''
        
        # Add before the main block
        content = content.replace(
            'if __name__ == "__main__":',
            cache_endpoint + '\nif __name__ == "__main__":'
        )
    
    # Write optimized file
    with open(api_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Unified API optimized with caching")

def create_performance_monitor():
    """Creëer performance monitoring"""
    print("🔧 Creating Performance Monitor...")
    
    monitor_content = '''"""
Performance Monitoring Utilities
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
        
        # Return all stats
        stats = {}
        endpoints = set()
        for key in self.metrics.keys():
            if key.endswith('_timing'):
                endpoints.add(key[:-7])  # Remove '_timing'
        
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
        except Exception as e:
            performance_monitor.record_error(endpoint)
            raise
    
    return wrapper
'''
    
    monitor_file = src_path / "performance_monitor.py"
    with open(monitor_file, 'w', encoding='utf-8') as f:
        f.write(monitor_content)
    
    print("✅ Performance Monitor created")

def main():
    print("🚀 Starting Performance Optimization...")
    print("=" * 60)
    
    try:
        # Run optimizations
        optimize_journal_engine()
        optimize_analytics_engine()
        create_caching_middleware()
        optimize_unified_api()
        create_performance_monitor()
        
        print("\n" + "=" * 60)
        print("🎉 Performance Optimization Complete!")
        print("\n📋 Next Steps:")
        print("1. Restart the API server to apply optimizations")
        print("2. Test the new cache endpoints: /api/cache/stats")
        print("3. Monitor performance improvements")
        print("4. Consider implementing Redis for production")
        
    except Exception as e:
        print(f"❌ Optimization failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
