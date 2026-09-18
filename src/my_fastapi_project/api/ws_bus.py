from redis.asyncio import Redis

from my_fastapi_project.api.ws_manager import manager

CHANNEL = "ws:broadcast"


async def publish(client: Redis, message: str) -> None:
    await client.publish(CHANNEL, message)


async def subscribe_loop(client: Redis) -> None:
    pubsub = client.pubsub()
    await pubsub.subscribe(CHANNEL)

    async for raw in pubsub.listen():
        if raw["type"] != "message":
            continue

        await manager.broadcast_local(raw["data"])
