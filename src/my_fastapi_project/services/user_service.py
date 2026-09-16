import asyncio
from typing import Any

from my_fastapi_project.core.exceptions import (
    EmailAlreadyExists,
    InvalidCredentials,
    InvalidOldPassword,
    UsernameAlreadyExists,
)
from my_fastapi_project.core.roles import ROLE_USER
from my_fastapi_project.core.security import hash_password, verify_password
from my_fastapi_project.repositories.user_repo import UserRepository
from my_fastapi_project.schemas.user import PasswordUpdate, UserCreate, UserUpdate


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def register(self, user: UserCreate) -> dict[str, Any]:
        if await self.repo.exists(user.username):
            raise UsernameAlreadyExists(user.username)
        if await self.repo.exists_email(user.email):
            raise EmailAlreadyExists(user.email)
        data = {
            "username": user.username,
            "email": user.email,
            "password": await asyncio.to_thread(hash_password, user.password),
            "role": ROLE_USER,
            "profile": user.profile.model_dump() if user.profile else None,
        }
        return await self.repo.create(user.username, data)

    async def get_user(self, username: str) -> dict[str, Any] | None:
        return await self.repo.get(username)

    async def list_users(self, offset: int, limit: int) -> list[dict[str, Any]]:
        users = await self.repo.list_all()
        return users[offset : offset + limit]

    async def change_password(self, username: str, data: PasswordUpdate) -> None:
        user = await self.repo.get(username)
        valid = user is not None and await asyncio.to_thread(
            verify_password, data.old_password, user["password"]
        )
        if not valid:
            raise InvalidOldPassword()
        new_password = await asyncio.to_thread(hash_password, data.new_password)
        await self.repo.update(username, {"password": new_password})

    async def update_user(
        self, username: str, data: UserUpdate
    ) -> dict[str, Any] | None:
        payload = data.model_dump(exclude_unset=True)
        return await self.repo.update(username, payload)

    async def delete_user(self, username: str) -> bool:
        return await self.repo.delete(username)

    async def authenticate(self, username: str, password: str) -> dict[str, Any]:
        user = await self.repo.get(username)
        valid = user is not None and await asyncio.to_thread(
            verify_password, password, user["password"]
        )
        if not valid:
            raise InvalidCredentials()
        return user
