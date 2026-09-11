from typing import Any

from my_fastapi_project.repositories.user_repo import UserRepository
from my_fastapi_project.schemas.user import PasswordUpdate, UserCreate, UserUpdate


def _hash_password(raw: str) -> str:
    return f"hashed_{raw}"


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def register(self, user: UserCreate) -> dict[str, Any] | None:
        if self.repo.exists(user.username):
            return None
        data = {
            "username": user.username,
            "email": user.email,
            "password": _hash_password(user.password),
            "profile": user.profile.model_dump() if user.profile else None,
        }
        return self.repo.create(user.username, data)

    def get_user(self, username: str) -> dict[str, Any] | None:
        return self.repo.get(username)

    def list_users(self, offset: int, limit: int) -> list[dict[str, Any]]:
        users = self.repo.list_all()
        return users[offset : offset + limit]

    def change_password(self, username: str, data: PasswordUpdate) -> bool:
        user = self.repo.get(username)
        if user is None:
            return False
        if user["password"] != _hash_password(data.old_password):
            return False
        self.repo.update(username, {"password": _hash_password(data.new_password)})
        return True

    def update_user(self, username: str, data: UserUpdate) -> dict[str, Any] | None:
        payload = data.model_dump(exclude_unset=True)
        return self.repo.update(username, payload)

    def delete_user(self, username: str) -> bool:
        return self.repo.delete(username)
