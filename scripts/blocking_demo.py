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


async def main() -> None:
    start = time.perf_counter()
    blocking_hash("预热")
    print(f"单次 bcrypt 哈希  : {time.perf_counter() - start:.3f} 秒")

    start = time.perf_counter()
    await asyncio.gather(*(fake_async_hash(f"假{i}") for i in range(3)))
    print(f"假异步 3 次哈希   : {time.perf_counter() - start:.2f} 秒")

    start = time.perf_counter()
    await asyncio.gather(*(real_async_hash(f"真{i}") for i in range(3)))
    print(f"外包后 3 次哈希   : {time.perf_counter() - start:.2f} 秒")


if __name__ == "__main__":
    asyncio.run(main())
