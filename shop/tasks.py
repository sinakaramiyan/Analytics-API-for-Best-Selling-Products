from celery import shared_task
from django.core.cache import cache
import logging,time

logger = logging.getLogger(__name__)

@shared_task
def clear_redis_cache():
    """Clear Redis cache at 2 AM daily"""
    try:
        logger.info("🕑 Starting scheduled Redis cache clearance (2 AM)...")
        cache.clear()
        logger.info("✅ Redis cache cleared successfully")
        return {"status": "success", "message": "Cache cleared at 2 AM"}
    except Exception as e:
        logger.error(f"❌ Failed to clear cache: {e}")
        return {"status": "error", "message": str(e)}

@shared_task
def test_celery_connection():
    """Test task to verify Celery is working"""
    print("✅ Celery is working correctly!")
    return "Celery test successful at " + time.strftime("%Y-%m-%d %H:%M:%S")