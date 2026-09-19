import asyncio
import logging

from redis.exceptions import ConnectionError as RedisConnectionError

from my_fastapi_project.api import ws_bus


class _DeadRedis:
    async def publish(self, channel: str, message: str) -> None:
        raise RedisConnectionError("模拟 Redis 不可用")


def test_publish_degrades_when_redis_is_down(caplog):
    with caplog.at_level(logging.WARNING):
        asyncio.run(ws_bus.publish(_DeadRedis(), "测试消息"))

    messages = [r.getMessage() for r in caplog.records]

    assert any("广播降级" in m for m in messages)
