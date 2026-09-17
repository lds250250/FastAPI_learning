import asyncio

from my_fastapi_project.core.redis import redis_client


async def main() -> None:
    print("一、连通性")
    print(f"   ping -> {await redis_client.ping()}")

    print()
    print("二、读写")
    await redis_client.set("greeting", "你好")
    print(f"   get('greeting') -> {await redis_client.get('greeting')!r}")

    print()
    print("三、过期时间")
    await redis_client.set("forever", "x")
    await redis_client.set("temp", "y", ex=10)
    print(
        f"   'forever' 的 ttl -> {await redis_client.ttl('forever')}   （-1 = 永不过期）"
    )
    print(
        f"   'temp' 的 ttl    -> {await redis_client.ttl('temp')}   （10 秒后自动消失）"
    )

    await redis_client.delete("greeting", "forever", "temp")
    print()
    print("已清理测试数据")

    await redis_client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
