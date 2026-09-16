import asyncio

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from my_fastapi_project.core.db import Base, enable_sqlite_foreign_keys
from my_fastapi_project.models import Book, User


async def open_test_db() -> tuple[AsyncEngine, async_sessionmaker]:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    enable_sqlite_foreign_keys(engine)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return engine, factory


def test_models_are_registered_in_metadata():
    assert sorted(Base.metadata.tables) == ["books", "borrow_records", "users"]


def test_book_roundtrip():
    asyncio.run(_book_roundtrip())


async def _book_roundtrip() -> None:
    engine, factory = await open_test_db()
    try:
        async with factory() as session:
            session.add(
                Book(
                    isbn="9787115428028",
                    title="流畅的Python",
                    author="Luciano Ramalho",
                    price=139.0,
                    stock=5,
                    internal_note="不外借",
                )
            )
            await session.commit()

        async with factory() as session:
            book = await session.get(Book, "9787115428028")
            assert book is not None
            assert book.title == "流畅的Python"
            assert book.stock == 5
            assert book.internal_note == "不外借"
    finally:
        await engine.dispose()


def test_profile_json_roundtrip():
    asyncio.run(_profile_roundtrip())


async def _profile_roundtrip() -> None:
    engine, factory = await open_test_db()
    try:
        async with factory() as session:
            session.add(
                User(
                    username="bob",
                    email="bob@example.com",
                    password="x" * 60,
                    role="user",
                    profile={"age": 30, "bio": "测试"},
                )
            )
            await session.commit()

        async with factory() as session:
            user = await session.get(User, "bob")
            assert user is not None
            assert user.profile == {"age": 30, "bio": "测试"}

            raw = (
                await session.execute(
                    text("SELECT profile FROM users WHERE username = 'bob'")
                )
            ).scalar()
            assert isinstance(raw, str)
    finally:
        await engine.dispose()


def test_duplicate_email_is_rejected():
    asyncio.run(_duplicate_email())


async def _duplicate_email() -> None:
    engine, factory = await open_test_db()
    try:
        async with factory() as session:
            session.add_all(
                [
                    User(
                        username="u1",
                        email="same@example.com",
                        password="x" * 60,
                        role="user",
                    ),
                    User(
                        username="u2",
                        email="same@example.com",
                        password="x" * 60,
                        role="user",
                    ),
                ]
            )
            with pytest.raises(IntegrityError):
                await session.commit()
    finally:
        await engine.dispose()
