# utils/decorators.py
from functools import wraps
from .cache_utils import cache_manager
import inspect

def auto_cache(key_prefix=None, timeout=None):
    """
    Decorator to automatically cache function results
    and repopulate on cache miss
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key based on function name and arguments
            if key_prefix:
                cache_key = key_prefix
            else:
                # Create key from function name and arguments
                arg_names = inspect.getfullargspec(func).args
                arg_dict = {}
                
                # Add positional arguments
                for i, arg in enumerate(args):
                    if i < len(arg_names):
                        arg_dict[arg_names[i]] = str(arg)
                
                # Add keyword arguments
                arg_dict.update({k: str(v) for k, v in kwargs.items()})
                
                cache_key = f"{func.__name__}:{hash(frozenset(arg_dict.items()))}"
            
            # Use get_or_set pattern
            def data_func():
                return func(*args, **kwargs)
            
            return cache_manager.get_or_set(cache_key, data_func, timeout)
        return wrapper
    return decorator