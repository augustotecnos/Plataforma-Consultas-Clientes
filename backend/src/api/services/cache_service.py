import redis.asyncio as redis
import json
import hashlib
from typing import Optional, Any, Dict
from src.core.config import settings

class CacheService:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            value = await self.redis_client.get(key)
            return json.loads(value) if value else None
        except Exception:
            return None
    
    async def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """Set value in cache with TTL"""
        try:
            ttl = ttl or settings.CACHE_TTL
            serialized = json.dumps(value, ensure_ascii=False, default=str)
            await self.redis_client.setex(key, ttl, serialized)
            return True
        except Exception:
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete key from cache"""
        try:
            await self.redis_client.delete(key)
            return True
        except Exception:
            return False
    
    async def delete_pattern(self, pattern: str) -> int:
        """Delete all keys matching pattern"""
        try:
            keys = await self.redis_client.keys(pattern)
            if keys:
                return await self.redis_client.delete(*keys)
            return 0
        except Exception:
            return 0
    
    def generate_search_key(self, **filters) -> str:
        """Generate unique cache key for search queries"""
        # Remove None values and sort for consistency
        clean_filters = {k: str(v).strip().lower() for k, v in filters.items() if v is not None}
        if not clean_filters:
            return "search:all"
        
        # Create deterministic hash
        filter_str = "_".join([f"{k}:{v}" for k, v in sorted(clean_filters.items())])
        hash_digest = hashlib.md5(filter_str.encode()).hexdigest()
        return f"search:{hash_digest}"
    
    def generate_client_key(self, client_id: int) -> str:
        """Generate cache key for individual client"""
        return f"client:{client_id}"
    
    async def get_client(self, client_id: int) -> Optional[Dict]:
        """Get client from cache"""
        key = self.generate_client_key(client_id)
        return await self.get(key)
    
    async def set_client(self, client_id: int, data: Dict, ttl: int = None) -> bool:
        """Cache client data"""
        key = self.generate_client_key(client_id)
        return await self.set(key, data, ttl or settings.CACHE_TTL)
    
    async def invalidate_client(self, client_id: int) -> bool:
        """Remove client from cache"""
        key = self.generate_client_key(client_id)
        return await self.delete(key)
    
    async def invalidate_search_cache(self) -> int:
        """Invalidate all search cache entries"""
        return await self.delete_pattern("search:*")
    
    async def health_check(self) -> bool:
        """Check Redis connection health"""
        try:
            await self.redis_client.ping()
            return True
        except Exception:
            return False
    
    async def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        try:
            info = await self.redis_client.info()
            return {
                "connected_clients": info.get("connected_clients", 0),
                "used_memory": info.get("used_memory_human", "0B"),
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0),
                "total_keys": len(await self.redis_client.keys("*"))
            }
        except Exception:
            return {"error": "Unable to fetch stats"}

# Global cache instance
cache_service = CacheService()
