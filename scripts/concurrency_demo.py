import asyncio
import time


async def job(name: str, seconds: float) -> str:
    await asyncio.sleep(seconds)
    return name


async def boom() -> str:
    await asyncio.sleep(0.1)
    raise ValueError("boom 炸了")


async def demo_one_by_one() -> None:
    start = time.perf_counter()
    await job("A", 1.0)
    await job("B", 1.0)
    print(f"逐个 await            : {time.perf_counter() - start:.2f} 秒")


async def demo_create_task() -> None:
    start = time.perf_counter()
    task_a = asyncio.create_task(job("A", 1.0))
    task_b = asyncio.create_task(job("B", 1.0))

    await asyncio.sleep(1.1)
    print(f"   1.1 秒时 task_a 完成了吗: {task_a.done()}")
    print(f"   1.1 秒时 task_b 完成了吗: {task_b.done()}")

    print(f"   收结果: {await task_a}, {await task_b}")
    print(f"create_task + 收结果  : {time.perf_counter() - start:.2f} 秒")


async def demo_gather() -> None:
    start = time.perf_counter()
    results = await asyncio.gather(job("A", 1.0), job("B", 1.0))
    print(f"gather                : {time.perf_counter() - start:.2f} 秒 -> {results}")


async def demo_gather_exception() -> None:
    try:
        await asyncio.gather(job("A", 0.5), boom())
    except ValueError as exc:
        print(f"   默认：异常直接抛给我 -> {exc!r}")

    results = await asyncio.gather(job("A", 0.5), boom(), return_exceptions=True)
    print(f"   return_exceptions=True -> {results}")


async def main() -> None:
    await demo_one_by_one()
    print()
    await demo_create_task()
    print()
    await demo_gather()
    print()
    await demo_gather_exception()


if __name__ == "__main__":
    asyncio.run(main())
