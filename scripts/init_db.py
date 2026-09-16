import asyncio

from sqlalchemy import text

from my_fastapi_project.core.db import Base, SessionFactory, engine
from my_fastapi_project.core.roles import ROLE_ADMIN, ROLE_USER
from my_fastapi_project.core.security import hash_password
from my_fastapi_project.models import Book, User


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("建表完成")


async def seed() -> None:
    async with SessionFactory() as session:
        if await session.get(User, "admin") is not None:
            print("已有种子数据，跳过")
            return

        session.add_all(
            [
                User(
                    username="admin",
                    email="admin@example.com",
                    password=hash_password("admin12345"),
                    role=ROLE_ADMIN,
                ),
                User(
                    username="alice",
                    email="alice@example.com",
                    password=hash_password("alice12345"),
                    role=ROLE_USER,
                    profile={"age": 28, "bio": "爱看书的后端新手"},
                ),
                Book(
                    isbn="9787115428028",
                    title="流畅的Python",
                    author="Luciano Ramalho",
                    price=139.0,
                    stock=5,
                    internal_note="馆藏重点，勿外借",
                ),
            ]
        )
        await session.commit()
        print("种子数据已写入")


async def show() -> None:
    async with SessionFactory() as session:
        for table in ("users", "books"):
            count = (
                await session.execute(text(f"SELECT COUNT(*) FROM {table}"))
            ).scalar()
            print(f"  {table}: {count} 行")

        profile = (
            await session.execute(
                text("SELECT profile FROM users WHERE username = 'alice'")
            )
        ).scalar()
        print(f"  alice 的 profile 原文: {profile!r}")


async def main() -> None:
    await create_tables()
    await seed()
    print("当前内容：")
    await show()
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
