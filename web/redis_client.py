# redis_client.py
import redis

client = redis.Redis(
    host='oregon-redis.render.com',
    port=6379,
    password='lZfHPBbmg8jwbrF0hmauCvJ0nAGQRJM4',
    username='red-csauologph6c73a6k100',
    ssl=True,
)

def get_redis_client():
    return client