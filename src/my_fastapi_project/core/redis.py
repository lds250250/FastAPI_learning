from redis.asyncio import Redis
from redis.exceptions import ConnectionError as RedisConnectionError
from redis.exceptions import TimeoutError as RedisTimeoutError

from my_fastapi_project.core.config import get_settings

settings = get_settings()

redis_client: Redis = Redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
)

RedisUnavailable = (RedisConnectionError, RedisTimeoutError)
