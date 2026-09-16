import pytest

from my_fastapi_project.repositories.user_repo import UserRepository


def make_user_data(
    username: str = "alice",
    email: str = "a@b.com",
    password: str = "hashed",
    role: str = "user",
    profile: dict | None = None,
) -> dict:
    return {
        "username": username,
        "email": email,
        "password": password,
        "role": role,
        "profile": profile,
    }


@pytest.mark.anyio
async def test_create_then_get(empty_user_repo: UserRepository):
    await empty_user_repo.create("alice", make_user_data())
    assert (await empty_user_repo.get("alice"))["email"] == "a@b.com"


@pytest.mark.anyio
async def test_get_missing_returns_none(empty_user_repo: UserRepository):
    assert await empty_user_repo.get("nobody") is None


@pytest.mark.anyio
async def test_exists(empty_user_repo: UserRepository):
    assert await empty_user_repo.exists("alice") is False
    await empty_user_repo.create("alice", make_user_data())
    assert await empty_user_repo.exists("alice") is True


@pytest.mark.anyio
async def test_update(empty_user_repo: UserRepository):
    await empty_user_repo.create("alice", make_user_data())
    await empty_user_repo.update("alice", {"email": "new@b.com"})
    assert (await empty_user_repo.get("alice"))["email"] == "new@b.com"


@pytest.mark.anyio
async def test_delete(empty_user_repo: UserRepository):
    await empty_user_repo.create("alice", make_user_data())
    assert await empty_user_repo.delete("alice") is True
    assert await empty_user_repo.delete("alice") is False


@pytest.mark.anyio
async def test_a_creates_alice(empty_user_repo: UserRepository):
    await empty_user_repo.create("alice", make_user_data())
    assert await empty_user_repo.exists("alice") is True


@pytest.mark.anyio
async def test_b_starts_empty(empty_user_repo: UserRepository):
    assert await empty_user_repo.exists("alice") is False
