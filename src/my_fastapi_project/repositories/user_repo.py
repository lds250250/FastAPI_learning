from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from my_fastapi_project.models import User


def _to_dict(user: User) -> dict[str, Any]:
    return {
        "username": user.username,
        "email": user.email,
        "password": user.password,
        "role": user.role,
        "profile": user.profile,
    }


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, username: str) -> dict[str, Any] | None:
        user = await self.session.get(User, username)
        return _to_dict(user) if user else None

    async def exists(self, username: str) -> bool:
        return await self.session.get(User, username) is not None

    async def list_all(
        self, offset: int = 0, limit: int | None = None
    ) -> list[dict[str, Any]]:
        stmt = select(User).order_by(User.username).offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)
        result = await self.session.execute(stmt)
        return [_to_dict(user) for user in result.scalars()]

    async def create(self, username: str, data: dict[str, Any]) -> dict[str, Any]:
        user = User(**data)
        self.session.add(user)
        await self.session.commit()
        return _to_dict(user)

    async def update(
        self, username: str, data: dict[str, Any]
    ) -> dict[str, Any] | None:
        user = await self.session.get(User, username)
        if user is None:
            return None
        for key, value in data.items():
            setattr(user, key, value)
        await self.session.commit()
        return _to_dict(user)

    async def delete(self, username: str) -> bool:
        user = await self.session.get(User, username)
        if user is None:
            return False
        await self.session.delete(user)
        await self.session.commit()
        return True

    async def exists_email(self, email: str) -> bool:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none() is not None
