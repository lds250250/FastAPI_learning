import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

TASKS = ["A", "B", "C"]
WAIT = 1.0


def blocking(name: str) -> str:
    time.sleep(WAIT)
    return name


async def non_blocking(name: str) -> str:
    await asyncio.sleep(WAIT)
    return name


def run_serial() -> float:
    # 1.串行
    start = time.perf_counter()
    for name in TASKS:
        blocking(name)
    return time.perf_counter() - start


def run_threads() -> float:
    # 2.多线程
    start = time.perf_counter()
    with ThreadPoolExecutor() as pool:
        list(pool.map(blocking, TASKS))
    return time.perf_counter() - start


async def run_async() -> float:
    # 3.异步
    start = time.perf_counter()
    await asyncio.gather(*(non_blocking(name) for name in TASKS))
    return time.perf_counter() - start


async def run_fake_async() -> float:
    # 4.假异步
    start = time.perf_counter()

    async def bad(name: str) -> str:
        return blocking(name)

    await asyncio.gather(*(bad(name) for name in TASKS))
    return time.perf_counter() - start


def main() -> None:
    print(f"① 串行（同步）    : {run_serial():.2f} 秒")
    print(f"② 多线程（并发）  : {run_threads():.2f} 秒")
    print(f"③ 异步（asyncio） : {asyncio.run(run_async()):.2f} 秒")
    print(f"④ 假异步（阻塞）  : {asyncio.run(run_fake_async()):.2f} 秒")


if __name__ == "__main__":
    main()
