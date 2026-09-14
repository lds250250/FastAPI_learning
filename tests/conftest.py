import pytest
from fastapi.testclient import TestClient

from my_fastapi_project.api.deps import ROLE_ADMIN, ROLE_USER, _hits, get_caller_role
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


@pytest.fixture
def auth_client(client):
    app.dependency_overrides[get_caller_role] = lambda: ROLE_USER
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def admin_client(client):
    app.dependency_overrides[get_caller_role] = lambda: ROLE_ADMIN
    yield client
    app.dependency_overrides.clear()
