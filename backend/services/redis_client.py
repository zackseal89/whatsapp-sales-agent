"""
Redis client wrapper for caching operations.
"""
import json
import logging
from typing import Optional, Any, Dict, List
import redis.asyncio as redis
from config import settings

logger = logging.getLogger(__name__)

class RedisCache:
    """Async Redis cache wrapper."""
    
    def __init__(self):
        self.redis: Optional[redis.Redis] = None
        self.enabled = settings.redis_enabled
        
        if self.enabled:
            try:
                self.redis = redis.from_url(
                    settings.redis_url,
                    encoding="utf-8",
                    decode_responses=True
                )
                # Test connection immediately
                # Note: We can't await in __init__, so we'll handle connection errors 
                # gracefully in the methods or use a startup event in FastAPI
                logger.info(f"Redis client initialized with URL: {settings.redis_url}")
            except Exception as e:
                logger.error(f"Failed to initialize Redis client: {e}")
                self.enabled = False

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if not self.enabled or not self.redis:
            return None
            
        try:
            value = await self.redis.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Redis get error for key {key}: {e}")
            return None

    async def set(self, key: str, value: Any, ttl: int = 300) -> bool:
        """Set value in cache with TTL."""
        if not self.enabled or not self.redis:
            return False
            
        try:
            json_value = json.dumps(value)
            await self.redis.setex(key, ttl, json_value)
            return True
        except Exception as e:
            logger.error(f"Redis set error for key {key}: {e}")
            return False

    async def delete(self, key: str) -> bool:
        """Delete value from cache."""
        if not self.enabled or not self.redis:
            return False
            
        try:
            await self.redis.delete(key)
            return True
        except Exception as e:
            logger.error(f"Redis delete error for key {key}: {e}")
            return False

    # Domain-specific helpers
    
    async def get_cached_conversation_history(self, conversation_id: str) -> Optional[List[Dict]]:
        """Get cached conversation history."""
        return await self.get(f"conversation:history:{conversation_id}")

    async def set_cached_conversation_history(self, conversation_id: str, messages: List[Dict], ttl: int = 300):
        """Cache conversation history."""
        await self.set(f"conversation:history:{conversation_id}", messages, ttl)

    async def invalidate_conversation_cache(self, conversation_id: str):
        """Invalidate conversation history cache."""
        await self.delete(f"conversation:history:{conversation_id}")

    async def get_cached_customer(self, whatsapp_number: str) -> Optional[Dict]:
        """Get cached customer data."""
        return await self.get(f"customer:{whatsapp_number}")

    async def set_cached_customer(self, whatsapp_number: str, customer: Dict, ttl: int = 1800):
        """Cache customer data."""
        await self.set(f"customer:{whatsapp_number}", customer, ttl)

# Global Redis client instance
redis_cache = RedisCache()
