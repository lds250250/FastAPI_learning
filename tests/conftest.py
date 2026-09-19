import asyncio
from pathlib import Path
from uuid import uuid4

import fakeredis.aioredis
import pytest
from fastapi.testclient import TestClient
from redis.exceptions import ConnectionError as RedisConnectionError
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from my_fastapi_project.api import ws_bus
from my_fastapi_project.api.deps import get_manager, get_redis, get_session
from my_fastapi_project.api.ws_manager import ConnectionManager
from my_fastapi_project.core.config import get_settings
from my_fastapi_project.core.db import Base
from my_fastapi_project.core.roles import ROLE_ADMIN, ROLE_USER
from my_fastapi_project.core.security import create_access_token, hash_password
from my_fastapi_project.main import app
from my_fastapi_project.models import Book, User
from my_fastapi_project.repositories.book_repo import BookRepository
from my_fastapi_project.repositories.user_repo import UserRepository

app.debug = False


SEED_PASSWORD = "secret123"
SEED_PASSWORD_HASH = hash_password(SEED_PASSWORD)


async def _create_all(engine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def _run(coro):
    return asyncio.run(coro)


@pytest.fixture
def db_factory():
    schema = f"test_{uuid4().hex[:8]}"

    engine = create_async_engine(
        get_settings().DATABASE_URL,
        poolclass=NullPool,
        connect_args={"server_settings": {"search_path": schema}},
        echo=False,
    )

    async def _setup() -> None:
        async with engine.begin() as conn:
            await conn.execute(text(f'CREATE SCHEMA "{schema}"'))

    async def _teardown() -> None:
        async with engine.begin() as conn:
            await conn.execute(text(f'DROP SCHEMA "{schema}" CASCADE'))
        await engine.dispose()

    _run(_setup())
    _run(_create_all(engine))

    yield async_sessionmaker(engine, expire_on_commit=False)

    _run(_teardown())


def seed_user(factory, username: str, role: str) -> None:
    async def _seed() -> None:
        async with factory() as session:
            session.add(
                User(
                    username=username,
                    email=f"{username}@b.com",
                    password=SEED_PASSWORD_HASH,
                    role=role,
                    profile=None,
                )
            )
            await session.commit()

    _run(_seed())


@pytest.fixture
def auth_client(client, db_factory):
    seed_user(db_factory, "caller", ROLE_USER)
    client.headers["Authorization"] = f"Bearer {create_access_token('caller')}"
    yield client
    client.headers.pop("Authorization", None)


@pytest.fixture
def admin_client(client, db_factory):
    seed_user(db_factory, "admin", ROLE_ADMIN)
    client.headers["Authorization"] = f"Bearer {create_access_token('admin')}"
    yield client
    client.headers.pop("Authorization", None)


@pytest.fixture
def sample_book(db_factory) -> str:
    isbn = "9787115428028"

    async def _seed() -> None:
        async with db_factory() as session:
            session.add(
                Book(
                    isbn=isbn,
                    title="流畅的Python",
                    author="Luciano Ramalho",
                    price=139.0,
                    stock=5,
                    internal_note=None,
                )
            )
            await session.commit()

    _run(_seed())
    return isbn


@pytest.fixture
async def empty_user_repo(db_factory):
    async with db_factory() as session:
        yield UserRepository(session)


@pytest.fixture
async def empty_book_repo(db_factory):
    async with db_factory() as session:
        yield BookRepository(session)


@pytest.fixture
def client(use_test_db):
    with TestClient(app) as c:
        yield c


@pytest.fixture
def use_test_db(db_factory):
    async def override_get_session():
        async with db_factory() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    yield
    app.dependency_overrides.pop(get_session, None)


@pytest.fixture
def alice(db_factory) -> str:
    seed_user(db_factory, "alice", ROLE_USER)
    return "alice"


@pytest.fixture
def ws_token(db_factory) -> str:
    seed_user(db_factory, "wsuser", ROLE_USER)
    return create_access_token("wsuser")


@pytest.fixture(autouse=True)
def fake_redis():
    client = fakeredis.aioredis.FakeRedis(decode_responses=True)
    app.dependency_overrides[get_redis] = lambda: client
    yield client
    app.dependency_overrides.pop(get_redis, None)


class DeadRedis:
    async def get(self, *args, **kwargs):
        raise RedisConnectionError("模拟 Redis 不可用")

    async def set(self, *args, **kwargs):
        raise RedisConnectionError("模拟 Redis 不可用")

    async def delete(self, *args, **kwargs):
        raise RedisConnectionError("模拟 Redis 不可用")

    async def incr(self, *args, **kwargs):
        raise RedisConnectionError("模拟 Redis 不可用")


@pytest.fixture
def dead_redis(fake_redis):
    app.dependency_overrides[get_redis] = lambda: DeadRedis()


@pytest.fixture
def ws_manager():
    fresh = ConnectionManager()
    app.dependency_overrides[get_manager] = lambda: fresh
    yield fresh
    app.dependency_overrides.pop(get_manager, None)


@pytest.fixture
def bob_token(db_factory) -> str:
    seed_user(db_factory, "bob", ROLE_USER)
    return create_access_token("bob")


@pytest.fixture
def admin_token(db_factory) -> str:
    seed_user(db_factory, "adminuser", ROLE_ADMIN)
    return create_access_token("adminuser")


@pytest.fixture(autouse=True)
def no_ws_subscribe(monkeypatch):
    async def noop(client):
        return

    monkeypatch.setattr(ws_bus, "subscribe_loop", noop)


@pytest.fixture
def local_ws_publish(monkeypatch, ws_manager):

    async def local_publish(client, message):
        await ws_manager.broadcast_local(message)

    monkeypatch.setattr(ws_bus, "publish", local_publish)
