import redis
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.environ["REDIS_URL"]
r = redis.Redis.from_url(REDIS_URL, decode_responses=True)


def check_rate_limit(user_ip: str, limit: int = 5, window: int = 60):
    key = f"rate:{user_ip}"
    count: int = r.incr(key, 1) #type: ignore
    if r.ttl(key) == -1:
        r.expire(key, window)
    return count > limit
