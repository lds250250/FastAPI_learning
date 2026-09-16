import pytest

from my_fastapi_project.core.exceptions import (
    EmailAlreadyExists,
    InvalidOldPassword,
    UsernameAlreadyExists,
)
from my_fastapi_project.repositories.user_repo import UserRepository
from my_fastapi_project.schemas.user import PasswordUpdate, UserCreate
from my_fastapi_project.services.user_service import UserService


@pytest.fixture
async def service(db_factory):
    async with db_factory() as session:
        yield UserService(UserRepository(session))


def make_user(
    username: str = "alice",
    email: str = "a@b.com",
    password: str = "secret123",
) -> UserCreate:
    return UserCreate(username=username, email=email, password=password)


@pytest.mark.anyio
async def test_register_creates_user(service):
    user = await service.register(make_user())

    assert user["username"] == "alice"
    assert user["email"] == "a@b.com"


@pytest.mark.anyio
async def test_register_does_not_store_plain_password(service):
    user = await service.register(make_user(password="secret123"))

    assert user["password"] != "secret123"


@pytest.mark.anyio
async def test_register_duplicate_username_raises(service):
    await service.register(make_user())

    with pytest.raises(UsernameAlreadyExists):
        await service.register(make_user(email="other@b.com"))


@pytest.mark.anyio
async def test_register_duplicate_email_raises(service):
    await service.register(make_user())

    with pytest.raises(EmailAlreadyExists):
        await service.register(make_user(username="bob"))


@pytest.mark.anyio
async def test_change_password_with_wrong_old_password_raises(service):
    await service.register(make_user(password="secret123"))

    with pytest.raises(InvalidOldPassword):
        await service.change_password(
            "alice",
            PasswordUpdate(old_password="wrongpass1", new_password="newsecret1"),
        )


@pytest.mark.anyio
async def test_change_password_makes_old_password_invalid(service):
    await service.register(make_user(password="secret123"))

    await service.change_password(
        "alice",
        PasswordUpdate(old_password="secret123", new_password="newsecret1"),
    )

    with pytest.raises(InvalidOldPassword):
        await service.change_password(
            "alice",
            PasswordUpdate(old_password="secret123", new_password="newsecret1"),
        )


@pytest.mark.anyio
async def test_get_user_returns_none_for_missing(service):
    assert await service.get_user("nobody") is None
