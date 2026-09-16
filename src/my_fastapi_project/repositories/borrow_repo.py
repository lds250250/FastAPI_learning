from datetime import UTC, datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from my_fastapi_project.models import BorrowRecord


def _to_dict(record: BorrowRecord) -> dict[str, Any]:
    return {
        "id": record.id,
        "username": record.username,
        "isbn": record.isbn,
        "borrowed_at": record.borrowed_at,
        "returned_at": record.returned_at,
    }


class BorrowRecordRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, username: str, isbn: str) -> dict[str, Any]:
        record = BorrowRecord(username=username, isbn=isbn)
        self.session.add(record)
        await self.session.commit()
        return _to_dict(record)

    async def get_open(self, username: str, isbn: str) -> dict[str, Any] | None:
        result = await self.session.execute(
            select(BorrowRecord)
            .where(
                BorrowRecord.username == username,
                BorrowRecord.isbn == isbn,
                BorrowRecord.returned_at.is_(None),
            )
            .order_by(BorrowRecord.borrowed_at.desc())
        )
        record = result.scalars().first()
        return _to_dict(record) if record else None

    async def close(self, record_id: int) -> None:
        record = await self.session.get(BorrowRecord, record_id)
        if record is None:
            return
        record.returned_at = datetime.now(UTC)
        await self.session.commit()

    async def list_by_username(self, username: str) -> list[dict[str, Any]]:
        result = await self.session.execute(
            select(BorrowRecord)
            .options(selectinload(BorrowRecord.book))
            .where(BorrowRecord.username == username)
            .order_by(BorrowRecord.borrowed_at.desc())
        )
        return [
            {**_to_dict(record), "title": record.book.title}
            for record in result.scalars()
        ]
