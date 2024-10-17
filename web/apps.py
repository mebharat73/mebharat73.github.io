from django.apps import AppConfig
import redis


class WebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web'

    def ready(self):
        # Create a Redis client
        self.redis_client = redis.StrictRedis(host='red-cs8c4dm8ii6s73c81j00', port=6379, decode_responses=True)
        try:
            self.redis_client.ping()
            print("Connected to Redis!")
        except redis.ConnectionError:
            print("Could not connect to Redis.")



