import asyncio
import time


async def hello() -> None:
    print("  ->'hello 执行了' 出现了")


async def worker(name: str, steps: int = 3) -> None:
    for i in range(steps):
        print(f"  {name} 第 {i} 步")
        await asyncio.sleep(0)


async def slow(name: str, seconds: float = 1.0) -> str:
    await asyncio.sleep(seconds)
    return name


async def demo_lazy() -> None:
    print("① 协程调用 ≠ 执行")
    coro = hello()
    print(f"   创建了：{type(coro).__name__}")
    print("   （上面没有出现 'hello 执行了'）")
    await coro
    print("   现在 await 它，才真的跑了")


async def demo_switching() -> None:
    print("② 证明「切换」真的发生")
    await asyncio.gather(worker("A"), worker("B"))


async def demo_await_is_waiting() -> None:
    print("③ await 是「等」，不是「启动」")

    start = time.perf_counter()
    await slow("A")
    await slow("B")
    print(f"   两次 await 分开写 : {time.perf_counter() - start:.2f} 秒")

    start = time.perf_counter()
    await asyncio.gather(slow("A"), slow("B"))
    print(f"   用 gather 一起等  : {time.perf_counter() - start:.2f} 秒")


async def main() -> None:
    await demo_lazy()
    print()
    await demo_switching()
    print()
    await demo_await_is_waiting()


if __name__ == "__main__":
    asyncio.run(main())
