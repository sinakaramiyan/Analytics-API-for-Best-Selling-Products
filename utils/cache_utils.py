from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

class RedisCacheManager:
    def __init__(self, key_prefix="app"):
        self.key_prefix = key_prefix
    
    def _get_full_key(self, key):
        return f"{self.key_prefix}:{key}"
    
    def set_data(self, key, data, timeout=None):
        """Store data in Redis cache"""
        try:
            full_key = self._get_full_key(key)
            cache.set(full_key, data, timeout)
            logger.info(f"Data cached with key: {full_key}")
            return True
        except Exception as e:
            logger.error(f"Error setting cache: {e}")
            return False
    
    def get_data(self, key):
        """Retrieve data from Redis cache"""
        try:
            full_key = self._get_full_key(key)
            data = cache.get(full_key)
            return data
        except Exception as e:
            logger.error(f"Error getting cache: {e}")
            return None
    
    def delete_data(self, key):
        """Delete specific key from cache"""
        try:
            full_key = self._get_full_key(key)
            cache.delete(full_key)
            return True
        except Exception as e:
            logger.error(f"Error deleting cache: {e}")
            return False
    
    def clear_all(self):
        """Clear all cache data (for 2 AM cleanup)"""
        try:
            cache.clear()
            logger.info("All cache data cleared")
            return True
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            return False
    
    def get_or_set(self, key, data_func, timeout=None):
        """Get data from cache or set it using the provided function"""
        data = self.get_data(key)
        if data is None:
            data = data_func()
            self.set_data(key, data, timeout)
        return data

# Global cache manager instance
cache_manager = RedisCacheManager(key_prefix="shop")