# # import redis
# # from ..core.config import Config

# # cache = redis.StrictRedis.from_url(Config().redis_url)

# # def set(key, value, ex=None):
# #     cache.set(key, value, ex=ex)

# # def get(key):
# #     return cache.get(key)
# import redis
# from .core.config import settings 
# from .config import CELERY_BROKER_URL  # Assuming Redis URL is the same as Celery's

# redis_client = redis.Redis.from_url(CELERY_BROKER_URL)

# def get_cached_subscription(subscription_id: int):
#     data = redis_client.get(f"subscription:{subscription_id}")
#     if data:
#         import json
#         return json.loads(data.decode('utf-8'))
#     return None

# def set_cached_subscription(subscription_id: int, subscription: dict):
#     import json
#     redis_client.setex(f"subscription:{subscription_id}", 3600, json.dumps(subscription)) # Cache for 1 hour

# def invalidate_cached_subscription(subscription_id: int):
#     redis_client.delete(f"subscription:{subscription_id}")
import redis
from .config import settings  # Import the settings object

def get_redis_client():
    """
    Returns a Redis client instance.
    """
    return redis.Redis(host=settings.redis_host, port=settings.redis_port)  # Use settings.redis_host and settings.redis_port


def set_cached_subscription(subscription_id: int, subscription_data: dict):
    """
    Caches a subscription in Redis.
    """
    redis_client = get_redis_client()
    key = f"subscription:{subscription_id}"
    redis_client.set(key, str(subscription_data))  # Store as string


def get_cached_subscription(subscription_id: int) -> dict | None:
    """
    Retrieves a subscription from the Redis cache.
    Returns None if not found.
    """
    redis_client = get_redis_client()
    key = f"subscription:{subscription_id}"
    data = redis_client.get(key)
    if data:
        try:
            return eval(data.decode())  # Evaluate the string back to a dict
        except (SyntaxError, NameError):
            return None  # Handle cases where the data is not a valid dict
    return None


def invalidate_cached_subscription(subscription_id: int):
    """
    Invalidates (deletes) a subscription from the Redis cache.
    """
    redis_client = get_redis_client()
    key = f"subscription:{subscription_id}"
    redis_client.delete(key)