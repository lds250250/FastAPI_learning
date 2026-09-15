import asyncio
import time

from my_fastapi_project.core.security import hash_password

PASSWORD = "correct-horse-battery"


def blocking_hash(label: str) -> str:
    hash_password(PASSWORD)
    return label


async def fake_async_hash(label: str) -> str:
    return blocking_hash(label)


async def real_async_hash(label: str) -> str:
    return await asyncio.to_thread(blocking_hash, label)


async def with_heartbeat(label: str, make_work) -> None:
    beats = 0

    async def heartbeat() -> None:
        nonlocal beats
        while True:
            await asyncio.sleep(0.05)
            beats += 1

    hb = asyncio.create_task(heartbeat())
    await asyncio.sleep(0)

    start = time.perf_counter()
    await make_work()
    elapsed = time.perf_counter() - start
    hb.cancel()
    print(f"{label}: 耗时 {elapsed:.2f}s，心跳 {beats} 次")


async def main() -> None:
    start = time.perf_counter()
    blocking_hash("预热")
    print(f"单次 bcrypt 哈希  : {time.perf_counter() - start:.3f} 秒")
    print()

    start = time.perf_counter()
    for i in range(3):
        blocking_hash(f"串行{i}")
    print(f"串行（不用协程）: {time.perf_counter() - start:.2f} 秒")
    print()

    await with_heartbeat(
        "假异步", lambda: asyncio.gather(*(fake_async_hash(f"假{i}") for i in range(3)))
    )
    await with_heartbeat(
        "外包后", lambda: asyncio.gather(*(real_async_hash(f"真{i}") for i in range(3)))
    )


if __name__ == "__main__":
    asyncio.run(main())
