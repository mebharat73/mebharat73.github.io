# web/apps.py
from django.apps import AppConfig
import redis

class WebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web'

    def ready(self):
        # Create a Redis client
        self.redis_client = redis.StrictRedis(host='redis://red-cs8c4dm8ii6s73c81j00', port=6379, decode_responses=True)
        try:
            self.redis_client.ping()
            print("Connected to Redis!")
        except redis.ConnectionError:
            print("Could not connect to Redis.")

    @staticmethod
    def get_redis_client():
        if not hasattr(WebConfig, '_redis_client'):
            WebConfig._redis_client = WebConfig().redis_client
        return WebConfig._redis_client