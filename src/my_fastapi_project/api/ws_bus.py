import logging

from redis.asyncio import Redis

from my_fastapi_project.api.ws_manager import manager
from my_fastapi_project.core.redis import RedisUnavailable

logger = logging.getLogger(__name__)

CHANNEL = "ws:broadcast"


async def publish(client: Redis, message: str) -> None:
    try:
        await client.publish(CHANNEL, message)
    except RedisUnavailable:
        logger.warning("Redis 不可用，广播降级（消息丢弃）：%s", message)


async def subscribe_loop(client: Redis) -> None:
    pubsub = client.pubsub()
    await pubsub.subscribe(CHANNEL)

    async for raw in pubsub.listen():
        if raw["type"] != "message":
            continue

        await manager.broadcast_local(raw["data"])
