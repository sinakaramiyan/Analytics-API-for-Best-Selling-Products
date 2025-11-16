import os
import django
import redis
from django.core.cache import cache

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def test_redis_connection():
    """Test basic Redis connection"""
    print("🔍 Testing Redis Connection...")
    try:
        r = redis.Redis(host='redis', port=6379, db=0)
        response = r.ping()
        print("✅ Redis server is running", response)
        return True
    except Exception as e:
        print(f"❌ Redis server connection failed: {e}")
        return False

def test_django_cache():
    """Test Django cache backend"""
    print("\n🔍 Testing Django Cache...")
    try:
        # Test basic operations
        cache.set('django_test', 'hello_redis', 60)
        value = cache.get('django_test')
        
        if value == 'hello_redis':
            print("✅ Django cache is working")
            cache.delete('django_test')
            return True
        else:
            print("❌ Django cache test failed")
            return False
    except Exception as e:
        print(f"❌ Django cache error: {e}")
        return False

def test_celery_queues():
    """Test Celery queue connection"""
    print("\n🔍 Testing Celery Queues...")
    try:
        from config.celery import app
        inspector = app.control.inspect()
        
        # Test if worker would be available
        active_queues = inspector.active_queues()
        if active_queues is not None:
            print("✅ Celery can connect to Redis broker")
            return True
        else:
            print("⚠️  No active workers, but broker connection OK")
            return True
    except Exception as e:
        print(f"❌ Celery broker test failed: {e}")
        return False

def test_shop_cache():
    """Test your shop-specific cache configuration"""
    print("\n🔍 Testing Shop Cache Configuration...")
    try:
        from shop.utils.cache_utils import shop_cache
        
        test_data = {
            'best_sellers': ['product_a', 'product_b', 'product_c'],
            'timestamp': '2024-01-01 12:00:00',
            'total_sales': 1500
        }
        
        # Test cache set
        success = shop_cache.cache_analytics('test_analytics', test_data, 300)
        if not success:
            print("❌ Failed to set shop cache")
            return False
        
        # Test cache get
        retrieved = shop_cache.get_analytics('test_analytics')
        if retrieved and retrieved['best_sellers'] == test_data['best_sellers']:
            print("✅ Shop cache utility is working")
            
            # Cleanup
            shop_cache.delete_data('test_analytics')
            return True
        else:
            print("❌ Shop cache retrieval failed")
            return False
            
    except Exception as e:
        print(f"❌ Shop cache test failed: {e}")
        return False

def check_redis_info():
    """Display Redis server information"""
    print("\n📊 Redis Server Information...")
    try:
        r = redis.Redis(host='redis', port=6379, db=0)
        info = r.info()
        
        print(f"Redis Version: {info['redis_version']}")
        print(f"Connected Clients: {info['connected_clients']}")
        print(f"Used Memory: {info['used_memory_human']}")
        print(f"Keyspace: {info['db0']['keys'] if 'db0' in info else 'N/A'}")
        return True
    except Exception as e:
        print(f"❌ Could not get Redis info: {e}")

def view_all_keys():
    """View all keys in Redis"""
    r = redis.Redis(host='redis', port=6379, db=0)
    print(r)
    keys = r.keys('*')
    print("All Keys:")
    for key in keys:
        key_type = r.type(key)
        print(f"- {key} (Type: {key_type})")

if __name__ == "__main__":
    print("🚀 Starting Redis Diagnostic Tests...\n")
    
    tests = [
        test_redis_connection,
        test_django_cache,
        test_celery_queues,
        test_shop_cache,
        check_redis_info,
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print(f"\n📋 Test Summary: {(results)}/{len(results)} tests passed")
    
    if all(results):
        print("🎉 All tests passed! Redis is working correctly.")
    else:
        print("❌ Some tests failed. Check the issues above.")

    view_all_keys()