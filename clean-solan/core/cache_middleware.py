"""
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
