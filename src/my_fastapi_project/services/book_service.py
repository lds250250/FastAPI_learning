from typing import Any

from my_fastapi_project.core.exceptions import (
    BookAlreadyExists,
    NotBorrowed,
    OutOfStock,
)
from my_fastapi_project.repositories.book_repo import BookRepository
from my_fastapi_project.repositories.borrow_repo import BorrowRecordRepository
from my_fastapi_project.schemas.book import BookCreate, BookUpdate


class BookService:
    def __init__(self, repo: BookRepository, record_repo: BorrowRecordRepository):
        self.repo = repo
        self.record_repo = record_repo

    async def create(self, book: BookCreate) -> dict[str, Any]:
        if await self.repo.exists(book.isbn):
            raise BookAlreadyExists(book.isbn)
        data = book.model_dump()
        return await self.repo.create(book.isbn, data)

    async def list_book(self, offset: int, limit: int) -> list[dict[str, Any]]:
        return await self.repo.list_all(offset, limit)

    async def get_book(self, isbn: str) -> dict[str, Any] | None:
        return await self.repo.get(isbn)

    async def update_book(self, isbn: str, data: BookUpdate) -> dict[str, Any] | None:
        payload = data.model_dump(exclude_unset=True)
        return await self.repo.update(isbn, payload)

    async def delete_book(self, isbn: str) -> bool:
        return await self.repo.delete(isbn)

    async def borrow(self, username: str, isbn: str) -> dict[str, Any]:
        if not await self.repo.decrement_stock(isbn):
            raise OutOfStock()
        await self.record_repo.create(username, isbn)
        return await self.repo.get(isbn)

    async def return_book(self, username: str, isbn: str) -> dict[str, Any]:
        record = await self.record_repo.get_open(username, isbn)
        if record is None:
            raise NotBorrowed()
        await self.record_repo.close(record["id"])
        await self.repo.increment_stock(isbn)
        return await self.repo.get(isbn)
