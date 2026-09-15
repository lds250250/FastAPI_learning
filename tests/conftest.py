import pytest
from fastapi.testclient import TestClient

from my_fastapi_project.api.deps import _hits
from my_fastapi_project.core.roles import ROLE_ADMIN, ROLE_USER
from my_fastapi_project.core.security import create_access_token, hash_password
from my_fastapi_project.main import app
from my_fastapi_project.repositories.book_repo import BookRepository, _books
from my_fastapi_project.repositories.user_repo import UserRepository, _users


@pytest.fixture(autouse=True)
def clean_state():
    _users.clear()
    _books.clear()
    _hits.clear()
    yield
    _users.clear()
    _books.clear()
    _hits.clear()


@pytest.fixture
def empty_user_repo() -> UserRepository:
    return UserRepository()


@pytest.fixture
def empty_book_repo() -> BookRepository:
    return BookRepository()


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def seed_user(username: str, role: str) -> None:
    _users[username] = {
        "username": username,
        "email": f"{username}@b.com",
        "password": hash_password("secret123"),
        "profile": None,
        "role": role,
    }


@pytest.fixture
def auth_client(client):
    seed_user("caller", ROLE_USER)
    token = create_access_token("caller")
    client.headers["Authorization"] = f"Bearer {token}"
    yield client


@pytest.fixture
def admin_client(client):
    """已登录的管理员客户端。"""
    seed_user("admin", ROLE_ADMIN)
    token = create_access_token("admin")
    client.headers["Authorization"] = f"Bearer {token}"
    yield client
