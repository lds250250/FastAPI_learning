import asyncio
import time
import uuid

from my_fastapi_project.core.redis import redis_client

TIMES = 5
WINDOW = 60
CONCURRENCY = 20


async def naive_limiter(key: str) -> bool:
    now = time.time()
    await redis_client.zremrangebyscore(key, 0, now - WINDOW)
    if await redis_client.zcard(key) >= TIMES:
        return False
    await redis_client.zadd(key, {uuid.uuid4().hex: now})
    await redis_client.expire(key, WINDOW)
    return True


async def fixed_window_limiter(key: str) -> bool:
    await redis_client.set(key, 0, ex=WINDOW)
    count = await redis_client.incr(key)
    return count <= TIMES


async def run(name: str, limiter) -> None:
    key = f"race:{name}"
    await redis_client.delete(key)

    results = await asyncio.gather(*[limiter(key) for _ in range(CONCURRENCY)])

    print(
        f"【{name}】限额 {TIMES}，并发发起 {CONCURRENCY} 次 → 实际放行 {sum(results)} 次"
    )

    await redis_client.delete(key)


async def main() -> None:
    await run("naive", naive_limiter)
    await run("incr", fixed_window_limiter)
    await redis_client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
