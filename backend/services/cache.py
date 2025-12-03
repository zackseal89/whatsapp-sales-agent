"""
Simple In-Memory Cache.
Replaces Redis with a local dictionary for zero-setup caching.
"""
import time
import logging
from typing import Optional, Any, Dict, List
from config import settings

logger = logging.getLogger(__name__)

class InMemoryCache:
    """
    Simple in-memory cache using a dictionary.
    Data is lost when the application restarts.
    """
    
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        logger.info("✅ In-Memory Cache initialized (Local RAM)")

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired."""
        if key not in self._cache:
            return None
            
        item = self._cache[key]
        
        # Check expiration
        if item['expires_at'] < time.time():
            del self._cache[key]
            return None
            
        return item['value']

    async def set(self, key: str, value: Any, ttl: int = 300) -> bool:
        """Set value in cache with TTL (seconds)."""
        try:
            self._cache[key] = {
                'value': value,
                'expires_at': time.time() + ttl
            }
            return True
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False

    async def delete(self, key: str) -> bool:
        """Delete value from cache."""
        if key in self._cache:
            del self._cache[key]
            return True
        return False

    # Domain-specific helpers (Same interface as before)
    
    async def get_cached_conversation_history(self, conversation_id: str) -> Optional[List[Dict]]:
        return await self.get(f"conversation:history:{conversation_id}")

    async def set_cached_conversation_history(self, conversation_id: str, messages: List[Dict], ttl: int = 300):
        await self.set(f"conversation:history:{conversation_id}", messages, ttl)

    async def invalidate_conversation_cache(self, conversation_id: str):
        await self.delete(f"conversation:history:{conversation_id}")

    async def get_cached_customer(self, whatsapp_number: str) -> Optional[Dict]:
        return await self.get(f"customer:{whatsapp_number}")

    async def set_cached_customer(self, whatsapp_number: str, customer: Dict, ttl: int = 1800):
        await self.set(f"customer:{whatsapp_number}", customer, ttl)

# Global Cache instance
# We keep the name 'redis_cache' temporarily to avoid breaking imports, 
# or we can rename it. Let's rename it to 'cache' in the new file.
cache = InMemoryCache()
