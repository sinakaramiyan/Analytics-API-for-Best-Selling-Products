from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

class ShopCacheManager:
    def __init__(self, prefix="shop"):
        self.prefix = prefix
    
    def _make_key(self, key):
        return f"{self.prefix}:{key}"
    
    def cache_analytics(self, key, data, timeout=86400):  # 24 hours
        """Cache shop analytics data"""
        try:
            full_key = self._make_key(key)
            cache.set(full_key, data, timeout)
            logger.info(f"Cached analytics data: {full_key}")
            return True
        except Exception as e:
            logger.error(f"Error caching data: {e}")
            return False
    
    def get_analytics(self, key):
        """Get cached analytics data"""
        try:
            full_key = self._make_key(key)
            return cache.get(full_key)
        except Exception as e:
            logger.error(f"Error getting cached data: {e}")
            return None
    
    def get_or_set_analytics(self, key, data_func, timeout=86400):
        """Get analytics data or set it using provided function"""
        data = self.get_analytics(key)
        if data is None:
            data = data_func()
            self.cache_analytics(key, data, timeout)
        return data
    
    def delete_data(self, key):
        """Delete specific key from cache"""
        try:
            full_key = self._make_key(key)
            cache.delete(full_key)
            return True
        except Exception as e:
            logger.error(f"Error deleting cache: {e}")
            return False


# Global instance
shop_cache = ShopCacheManager()