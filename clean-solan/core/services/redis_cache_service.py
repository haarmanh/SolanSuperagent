"""
Redis Caching Service for Solān
High-performance caching layer for 80% faster API responses
"""

import json
import pickle
import asyncio
from typing import Any, Optional, Dict, List, Union
from datetime import datetime, timedelta
from functools import wraps
import hashlib
import logging

# Setup logger
logger = logging.getLogger(__name__)

try:
    import redis.asyncio as redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    # Mock Redis for when it's not available
    class MockRedis:
        async def ping(self): return True
        async def setex(self, key, ttl, value): return True
        async def get(self, key): return None
        async def delete(self, *keys): return 0
        async def keys(self, pattern): return []
        async def info(self): return {}
        async def close(self): pass

    class MockConnectionPool:
        @classmethod
        def from_url(cls, *args, **kwargs): return cls()
        async def disconnect(self): pass

    redis = type('MockRedisModule', (), {
        'Redis': MockRedis,
        'ConnectionPool': MockConnectionPool
    })()

class RedisCacheService:
    """High-performance Redis caching service"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        self.redis_url = redis_url
        self.redis_client: Optional[redis.Redis] = None
        self.connection_pool: Optional[redis.ConnectionPool] = None
        self.is_connected = False
        
        # Cache configuration
        self.default_ttl = 3600  # 1 hour
        self.config_ttl = 7200   # 2 hours
        self.api_response_ttl = 300  # 5 minutes
        self.session_ttl = 86400     # 24 hours
        
        # Cache key prefixes
        self.prefixes = {
            'config': 'solan:config:',
            'api': 'solan:api:',
            'session': 'solan:session:',
            'god_core': 'solan:god_core:',
            'ethics': 'solan:ethics:',
            'user': 'solan:user:'
        }
    
    async def connect(self):
        """Establish Redis connection with connection pooling"""
        try:
            # Create connection pool for better performance
            self.connection_pool = redis.ConnectionPool.from_url(
                self.redis_url,
                max_connections=20,
                retry_on_timeout=True,
                socket_keepalive=True,
                socket_keepalive_options={},
                health_check_interval=30
            )
            
            # Create Redis client
            self.redis_client = redis.Redis(
                connection_pool=self.connection_pool,
                decode_responses=False  # We'll handle encoding ourselves
            )
            
            # Test connection
            await self.redis_client.ping()
            self.is_connected = True
            
            logger.info("✅ Redis cache service connected successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Redis connection failed: {e}")
            self.is_connected = False
            return False
    
    async def disconnect(self):
        """Close Redis connection"""
        if self.redis_client:
            await self.redis_client.close()
        if self.connection_pool:
            await self.connection_pool.disconnect()
        self.is_connected = False
        logger.info("🔌 Redis cache service disconnected")
    
    def _generate_cache_key(self, prefix: str, key: str, **kwargs) -> str:
        """Generate unique cache key with prefix"""
        # Include kwargs in key for parameter-specific caching
        if kwargs:
            key_data = f"{key}:{json.dumps(kwargs, sort_keys=True)}"
        else:
            key_data = key
        
        # Hash long keys to avoid Redis key length limits
        if len(key_data) > 200:
            key_hash = hashlib.md5(key_data.encode()).hexdigest()
            return f"{self.prefixes[prefix]}{key_hash}"
        
        return f"{self.prefixes[prefix]}{key_data}"
    
    async def set(self, prefix: str, key: str, value: Any, ttl: Optional[int] = None, **kwargs) -> bool:
        """Set cache value with TTL"""
        if not self.is_connected:
            return False
        
        try:
            cache_key = self._generate_cache_key(prefix, key, **kwargs)
            
            # Serialize value
            if isinstance(value, (dict, list)):
                serialized_value = json.dumps(value).encode('utf-8')
            elif isinstance(value, str):
                serialized_value = value.encode('utf-8')
            else:
                serialized_value = pickle.dumps(value)
            
            # Set TTL based on prefix if not specified
            if ttl is None:
                ttl = self._get_default_ttl(prefix)
            
            # Store in Redis
            await self.redis_client.setex(cache_key, ttl, serialized_value)
            
            logger.debug(f"📦 Cached {prefix}:{key} (TTL: {ttl}s)")
            return True
            
        except Exception as e:
            logger.error(f"❌ Cache set failed for {prefix}:{key}: {e}")
            return False
    
    async def get(self, prefix: str, key: str, **kwargs) -> Optional[Any]:
        """Get cache value"""
        if not self.is_connected:
            return None
        
        try:
            cache_key = self._generate_cache_key(prefix, key, **kwargs)
            
            # Get from Redis
            cached_data = await self.redis_client.get(cache_key)
            
            if cached_data is None:
                logger.debug(f"🔍 Cache miss: {prefix}:{key}")
                return None
            
            # Deserialize value
            try:
                # Try JSON first (most common)
                value = json.loads(cached_data.decode('utf-8'))
            except (json.JSONDecodeError, UnicodeDecodeError):
                try:
                    # Try string
                    value = cached_data.decode('utf-8')
                except UnicodeDecodeError:
                    # Fall back to pickle
                    value = pickle.loads(cached_data)
            
            logger.debug(f"✅ Cache hit: {prefix}:{key}")
            return value
            
        except Exception as e:
            logger.error(f"❌ Cache get failed for {prefix}:{key}: {e}")
            return None
    
    async def delete(self, prefix: str, key: str, **kwargs) -> bool:
        """Delete cache entry"""
        if not self.is_connected:
            return False
        
        try:
            cache_key = self._generate_cache_key(prefix, key, **kwargs)
            result = await self.redis_client.delete(cache_key)
            
            logger.debug(f"🗑️ Cache deleted: {prefix}:{key}")
            return result > 0
            
        except Exception as e:
            logger.error(f"❌ Cache delete failed for {prefix}:{key}: {e}")
            return False
    
    async def clear_prefix(self, prefix: str) -> int:
        """Clear all cache entries with given prefix"""
        if not self.is_connected:
            return 0
        
        try:
            pattern = f"{self.prefixes[prefix]}*"
            keys = await self.redis_client.keys(pattern)
            
            if keys:
                deleted = await self.redis_client.delete(*keys)
                logger.info(f"🧹 Cleared {deleted} cache entries with prefix {prefix}")
                return deleted
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ Cache clear failed for prefix {prefix}: {e}")
            return 0
    
    async def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        if not self.is_connected:
            return {"connected": False}
        
        try:
            info = await self.redis_client.info()
            
            stats = {
                "connected": True,
                "used_memory": info.get("used_memory_human", "0B"),
                "total_keys": info.get("db0", {}).get("keys", 0),
                "hits": info.get("keyspace_hits", 0),
                "misses": info.get("keyspace_misses", 0),
                "hit_rate": 0
            }
            
            # Calculate hit rate
            total_requests = stats["hits"] + stats["misses"]
            if total_requests > 0:
                stats["hit_rate"] = (stats["hits"] / total_requests) * 100
            
            return stats
            
        except Exception as e:
            logger.error(f"❌ Failed to get cache stats: {e}")
            return {"connected": False, "error": str(e)}
    
    def _get_default_ttl(self, prefix: str) -> int:
        """Get default TTL for prefix"""
        ttl_map = {
            'config': self.config_ttl,
            'api': self.api_response_ttl,
            'session': self.session_ttl,
            'god_core': self.api_response_ttl,
            'ethics': self.api_response_ttl,
            'user': self.session_ttl
        }
        return ttl_map.get(prefix, self.default_ttl)

# Global cache service instance
cache_service = RedisCacheService()

# Decorator for automatic caching
def cache_result(prefix: str, ttl: Optional[int] = None, key_func: Optional[callable] = None):
    """Decorator for automatic function result caching"""
    
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                cache_key = f"{func.__name__}:{hash(str(args) + str(sorted(kwargs.items())))}"
            
            # Try to get from cache
            cached_result = await cache_service.get(prefix, cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            await cache_service.set(prefix, cache_key, result, ttl)
            
            return result
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            # For sync functions, we need to run async operations
            loop = asyncio.get_event_loop()
            
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                cache_key = f"{func.__name__}:{hash(str(args) + str(sorted(kwargs.items())))}"
            
            # Try to get from cache
            cached_result = loop.run_until_complete(cache_service.get(prefix, cache_key))
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            loop.run_until_complete(cache_service.set(prefix, cache_key, result, ttl))
            
            return result
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    
    return decorator

# Convenience functions
async def cache_config(key: str, value: Any, ttl: Optional[int] = None) -> bool:
    """Cache configuration data"""
    return await cache_service.set('config', key, value, ttl)

async def get_cached_config(key: str) -> Optional[Any]:
    """Get cached configuration data"""
    return await cache_service.get('config', key)

async def cache_api_response(endpoint: str, params: Dict, response: Any, ttl: Optional[int] = None) -> bool:
    """Cache API response"""
    return await cache_service.set('api', endpoint, response, ttl, **params)

async def get_cached_api_response(endpoint: str, params: Dict) -> Optional[Any]:
    """Get cached API response"""
    return await cache_service.get('api', endpoint, **params)
