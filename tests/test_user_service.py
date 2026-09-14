import pytest

from my_fastapi_project.core.exceptions import (
    EmailAlreadyExists,
    InvalidOldPassword,
    UsernameAlreadyExists,
)
from my_fastapi_project.schemas.user import PasswordUpdate, UserCreate
from my_fastapi_project.services.user_service import UserRepository, UserService


@pytest.fixture
def service() -> UserService:
    return UserService(UserRepository())


def make_user(
    username: str = "alice",
    email: str = "a@b.com",
    password: str = "secret123",
) -> UserCreate:
    return UserCreate(username=username, email=email, password=password)


def test_register_creates_user(service):
    user = service.register(make_user())

    assert user["username"] == "alice"
    assert user["email"] == "a@b.com"


def test_register_does_not_store_plain_password(service):
    user = service.register(make_user(password="secret123"))

    assert user["password"] != "secret123"


def test_register_duplicate_username_raises(service):
    service.register(make_user())

    with pytest.raises(UsernameAlreadyExists):
        service.register(make_user(email="other@b.com"))


def test_register_duplicate_email_raises(service):
    service.register(make_user())

    with pytest.raises(EmailAlreadyExists):
        service.register(make_user(username="bob"))


def test_change_password_with_wrong_old_password_raises(service):
    service.register(make_user(password="secret123"))

    with pytest.raises(InvalidOldPassword):
        service.change_password(
            "alice",
            PasswordUpdate(old_password="wrongpass1", new_password="newsecret1"),
        )


def test_change_password_makes_old_password_invalid(service):
    service.register(make_user(password="secret123"))

    service.change_password(
        "alice",
        PasswordUpdate(old_password="secret123", new_password="newsecret1"),
    )

    with pytest.raises(InvalidOldPassword):
        service.change_password(
            "alice",
            PasswordUpdate(old_password="secret123", new_password="newsecret1"),
        )


def test_get_user_returns_none_for_missing(service):
    assert service.get_user("nobody") is None
