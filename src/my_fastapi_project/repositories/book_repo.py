from typing import Any

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from my_fastapi_project.models import Book


def _to_dict(book: Book) -> dict[str, Any]:
    return {
        "isbn": book.isbn,
        "title": book.title,
        "author": book.author,
        "price": book.price,
        "stock": book.stock,
        "internal_note": book.internal_note,
    }


class BookRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, isbn: str, data: dict[str, Any]) -> dict[str, Any]:
        book = Book(**data)
        self.session.add(book)
        await self.session.commit()
        return _to_dict(book)

    async def exists(self, isbn: str) -> bool:
        return await self.session.get(Book, isbn) is not None

    async def get(self, isbn: str) -> dict[str, Any] | None:
        book = await self.session.get(Book, isbn)
        return _to_dict(book) if book else None

    async def list_all(
        self, offset: int = 0, limit: int | None = None
    ) -> list[dict[str, Any]]:
        stmt = select(Book).order_by(Book.isbn).offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)
        result = await self.session.execute(stmt)
        return [_to_dict(book) for book in result.scalars()]

    async def update(self, isbn: str, data: dict[str, Any]) -> dict[str, Any] | None:
        book = await self.session.get(Book, isbn)
        if book is None:
            return None
        for key, value in data.items():
            setattr(book, key, value)
        await self.session.commit()
        return _to_dict(book)

    async def delete(self, isbn: str) -> bool:
        book = await self.session.get(Book, isbn)
        if book is None:
            return False
        await self.session.delete(book)
        await self.session.commit()
        return True

    async def decrement_stock(self, isbn: str) -> bool:
        """原子地把库存减 1。True 表示扣减成功，False 表示没库存了。"""
        result = await self.session.execute(
            update(Book)
            .where(Book.isbn == isbn, Book.stock > 0)
            .values(stock=Book.stock - 1)
        )
        await self.session.commit()
        return result.rowcount == 1

    async def increment_stock(self, isbn: str) -> None:
        await self.session.execute(
            update(Book).where(Book.isbn == isbn).values(stock=Book.stock + 1)
        )
        await self.session.commit()
