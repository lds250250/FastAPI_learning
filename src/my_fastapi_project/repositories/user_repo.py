from typing import Any

# 进程级假数据库：放模块顶层，所有 UserRepository 实例共享同一份数据
_users: dict[str, dict[str, Any]] = {}


class UserRepository:
    def get(self, username: str) -> dict[str, Any] | None:
        return _users.get(username)

    def exists(self, username: str) -> bool:
        return username in _users

    def list_all(self) -> list[dict[str, Any]]:
        return list(_users.values())

    def create(self, username: str, data: dict[str, Any]) -> dict[str, Any]:
        _users[username] = data
        return _users[username]

    def update(self, username: str, data: dict[str, Any]) -> dict[str, Any] | None:
        user = _users.get(username)
        if user is None:
            return None
        user.update(data)
        return user

    def delete(self, username: str) -> bool:
        return _users.pop(username, None) is not None

    def exists_email(self, email: str) -> bool:
        return any(u["email"] == email for u in _users.values())
