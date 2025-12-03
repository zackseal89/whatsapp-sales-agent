import asyncio
import logging
from services.redis_client import redis_cache

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_cache():
    print("🧪 Testing Redis Cache...")
    
    if not redis_cache.enabled:
        print("⚠️ Redis is disabled or unavailable. Testing graceful degradation...")
        
        # Test get (should return None)
        val = await redis_cache.get("test_key")
        assert val is None
        print("✅ Graceful get passed")
        
        # Test set (should return False)
        success = await redis_cache.set("test_key", "value")
        assert success is False
        print("✅ Graceful set passed")
        
        print("✅ Graceful degradation verified!")
        return

    print("✅ Redis is enabled and connected!")
    
    # Test 1: Basic Set/Get
    print("\nTest 1: Basic Set/Get")
    test_data = {"foo": "bar", "num": 123}
    await redis_cache.set("test_key", test_data, ttl=60)
    result = await redis_cache.get("test_key")
    assert result == test_data
    print(f"✅ Set/Get passed: {result}")
    
    # Test 2: Conversation History
    print("\nTest 2: Conversation History")
    history = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"}
    ]
    await redis_cache.set_cached_conversation_history("test-convo-123", history)
    cached_history = await redis_cache.get_cached_conversation_history("test-convo-123")
    assert cached_history == history
    print(f"✅ History caching passed: {len(cached_history)} messages")
    
    # Test 3: Invalidation
    print("\nTest 3: Cache Invalidation")
    await redis_cache.invalidate_conversation_cache("test-convo-123")
    deleted = await redis_cache.get_cached_conversation_history("test-convo-123")
    assert deleted is None
    print("✅ Invalidation passed")
    
    # Test 4: Customer Caching
    print("\nTest 4: Customer Caching")
    customer = {"id": "cust-123", "name": "Test User"}
    await redis_cache.set_cached_customer("1234567890", customer)
    cached_cust = await redis_cache.get_cached_customer("1234567890")
    assert cached_cust == customer
    print("✅ Customer caching passed")

    print("\n🎉 All Redis tests passed successfully!")

if __name__ == "__main__":
    asyncio.run(test_cache())
