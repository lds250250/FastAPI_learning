import asyncio

import pytest
from sqlalchemy.exc import IntegrityError

from my_fastapi_project.core.db import Base
from my_fastapi_project.models import Book, User


def test_models_are_registered_in_metadata():
    assert sorted(Base.metadata.tables) == ["books", "borrow_records", "users"]


def test_book_roundtrip(db_factory):
    asyncio.run(_book_roundtrip(db_factory))


async def _book_roundtrip(factory) -> None:
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


def test_profile_json_roundtrip(db_factory):
    asyncio.run(_profile_roundtrip(db_factory))


async def _profile_roundtrip(factory) -> None:
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


def test_duplicate_email_is_rejected(db_factory):
    asyncio.run(_duplicate_email(db_factory))


async def _duplicate_email(factory) -> None:
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
