import asyncio

from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import create_async_engine

from my_fastapi_project.core.db import engine


async def show_lazy() -> None:
    print("一、建引擎是惰性的：指向不存在的目录也不会报错")
    throwaway = create_async_engine("sqlite+aiosqlite:///./no_such_dir/app.db")
    print("   引擎建好了，没有任何异常")

    try:
        async with throwaway.connect() as conn:
            await conn.execute(text("SELECT 1"))
        print("   竟然连上了？")
    except OperationalError as exc:
        print(f"  真去连的时候才报错 -> {exc.orig}")
    finally:
        await throwaway.dispose()


async def check_app_engine() -> None:
    print()
    print("二、真正有用的检查：用应用自己的引擎连一次")
    print(f"   URL = {engine.url}")
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT 1"))
        print(f"  SELECT 1 -> {result.scalar()}")
    await engine.dispose()


async def check_foreign_keys() -> None:
    print()
    print("三、外键约束有没有真的打开")
    async with engine.connect() as conn:
        enabled = (await conn.execute(text("PRAGMA foreign_keys"))).scalar()
    print(f"   PRAGMA foreign_keys = {enabled}（1 表示已启用）")


async def main() -> None:
    await show_lazy()
    await check_app_engine()
    await check_foreign_keys()


if __name__ == "__main__":
    asyncio.run(main())
