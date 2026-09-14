import pytest
from fastapi.testclient import TestClient

from my_fastapi_project.api.deps import _hits
from my_fastapi_project.main import app
from my_fastapi_project.repositories.book_repo import _books
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
def client():
    with TestClient(app) as c:
        yield c
