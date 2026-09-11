import pytest

from my_fastapi_project.repositories.user_repo import UserRepository, _users


@pytest.fixture
def empty_user_repo():
    _users.clear()
    yield UserRepository()
    _users.clear()
