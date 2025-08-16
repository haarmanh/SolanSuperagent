"""
Optimized async configuration loader with Redis caching
"""

import aiofiles
import json
import os
from functools import lru_cache
from typing import Dict, Any, Optional
from pathlib import Path

# Import Redis cache service
try:
    from .services.redis_cache_service import cache_service, cache_config, get_cached_config
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

class ConfigCache:
    """High-performance configuration cache with Redis backend"""

    def __init__(self):
        self._local_cache: Dict[str, Any] = {}
        self._redis_enabled = REDIS_AVAILABLE and os.getenv('REDIS_ENABLED', 'true').lower() == 'true'

    async def ensure_redis_connection(self):
        """Ensure Redis connection is established"""
        if self._redis_enabled and cache_service and not cache_service.is_connected:
            await cache_service.connect()

    async def load_config(self, config_file: str) -> Dict[str, Any]:
        """Load configuration with Redis + local caching"""

        config_path = Path(config_file)
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_file}")

        cache_key = str(config_path.absolute())

        # Try Redis cache first (if enabled)
        if self._redis_enabled:
            await self.ensure_redis_connection()
            cached_config = await get_cached_config(cache_key)
            if cached_config is not None:
                self._local_cache[cache_key] = cached_config
                return cached_config

        # Try local cache
        if cache_key in self._local_cache:
            return self._local_cache[cache_key]

        # Load from file
        try:
            async with aiofiles.open(config_path, 'r', encoding='utf-8') as f:
                content = await f.read()
                config_data = json.loads(content)

                # Cache in both local and Redis
                self._local_cache[cache_key] = config_data

                if self._redis_enabled:
                    await cache_config(cache_key, config_data)

                return config_data

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {config_file}: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to load config {config_file}: {e}")

    def get_cached_config(self, config_file: str) -> Optional[Dict[str, Any]]:
        """Get cached configuration from local cache only"""
        cache_key = str(Path(config_file).absolute())
        return self._local_cache.get(cache_key)

    async def clear_cache(self):
        """Clear all configuration caches"""
        self._local_cache.clear()

        if self._redis_enabled and cache_service:
            await cache_service.clear_prefix('config')

    async def invalidate_config(self, config_file: str):
        """Invalidate specific configuration"""
        cache_key = str(Path(config_file).absolute())

        # Remove from local cache
        self._local_cache.pop(cache_key, None)

        # Remove from Redis cache
        if self._redis_enabled and cache_service:
            await cache_service.delete('config', cache_key)

# Global config cache instance
config_cache = ConfigCache()

async def load_config_async(config_file: str) -> Dict[str, Any]:
    """Async configuration loader with caching"""
    return await config_cache.load_config(config_file)

def get_config_sync(config_file: str) -> Optional[Dict[str, Any]]:
    """Get cached configuration synchronously"""
    return config_cache.get_cached_config(config_file)
