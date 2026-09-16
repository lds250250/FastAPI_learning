from typing import Any

from my_fastapi_project.core.exceptions import BookAlreadyExists, OutOfStock
from my_fastapi_project.repositories.book_repo import BookRepository
from my_fastapi_project.schemas.book import BookCreate, BookUpdate


class BookService:
    def __init__(self, repo: BookRepository):
        self.repo = repo

    async def create(self, book: BookCreate) -> dict[str, Any]:
        if await self.repo.exists(book.isbn):
            raise BookAlreadyExists(book.isbn)
        data = book.model_dump()
        return await self.repo.create(book.isbn, data)

    async def list_book(self, offset: int, limit: int) -> list[dict[str, Any]]:
        books = await self.repo.list_all()
        return books[offset : offset + limit]

    async def get_book(self, isbn: str) -> dict[str, Any] | None:
        return await self.repo.get(isbn)

    async def update_book(self, isbn: str, data: BookUpdate) -> dict[str, Any] | None:
        payload = data.model_dump(exclude_unset=True)
        return await self.repo.update(isbn, payload)

    async def delete_book(self, isbn: str) -> bool:
        return await self.repo.delete(isbn)

    async def borrow(self, isbn: str) -> dict[str, Any]:
        book = await self.repo.get(isbn)
        if book is None:
            raise OutOfStock()
        if book["stock"] == 0:
            raise OutOfStock()
        await self.repo.update(isbn, {"stock": book["stock"] - 1})
        return await self.repo.get(isbn)
