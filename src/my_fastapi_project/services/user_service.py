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

    def register(self, user: UserCreate) -> dict[str, Any]:
        if self.repo.exists(user.username):
            raise UsernameAlreadyExists(user.username)
        if self.repo.exists_email(user.email):
            raise EmailAlreadyExists(user.email)
        data = {
            "username": user.username,
            "email": user.email,
            "password": hash_password(user.password),
            "role": ROLE_USER,
            "profile": user.profile.model_dump() if user.profile else None,
        }
        return self.repo.create(user.username, data)

    def get_user(self, username: str) -> dict[str, Any] | None:
        return self.repo.get(username)

    def list_users(self, offset: int, limit: int) -> list[dict[str, Any]]:
        users = self.repo.list_all()
        return users[offset : offset + limit]

    def change_password(self, username: str, data: PasswordUpdate) -> None:
        user = self.repo.get(username)
        if user is None or not verify_password(data.old_password, user["password"]):
            raise InvalidOldPassword()
        self.repo.update(username, {"password": hash_password(data.new_password)})

    def update_user(self, username: str, data: UserUpdate) -> dict[str, Any] | None:
        payload = data.model_dump(exclude_unset=True)
        return self.repo.update(username, payload)

    def delete_user(self, username: str) -> bool:
        return self.repo.delete(username)

    def authenticate(self, username: str, password: str) -> dict[str, Any]:
        user = self.repo.get(username)
        if user is None or not verify_password(password, user["password"]):
            raise InvalidCredentials()
        return user
