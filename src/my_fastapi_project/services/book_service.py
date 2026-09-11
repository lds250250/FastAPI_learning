from typing import Any

from my_fastapi_project.core.exceptions import BookAlreadyExists, OutOfStock
from my_fastapi_project.repositories.book_repo import BookRepository
from my_fastapi_project.schemas.book import BookCreate, BookUpdate


class BookService:
    def __init__(self, repo: BookRepository):
        self.repo = repo

    def create(self, book: BookCreate) -> dict[str, Any]:
        if self.repo.exists(book.isbn):
            raise BookAlreadyExists(book.isbn)
        data = book.model_dump()
        return self.repo.create(book.isbn, data)

    def list_book(self, offset: int, limit: int) -> list[dict[str, Any]]:
        books = self.repo.list_all()
        return books[offset : offset + limit]

    def get_book(self, isbn: str) -> dict[str, Any] | None:
        return self.repo.get(isbn)

    def update_book(self, isbn: str, data: BookUpdate) -> dict[str, Any] | None:
        payload = data.model_dump(exclude_unset=True)
        return self.repo.update(isbn, payload)

    def delete_book(self, isbn: str) -> bool:
        return self.repo.delete(isbn)

    def borrow(self, isbn: str) -> dict[str, Any]:
        book = self.repo.get(isbn)
        if book is None:
            raise OutOfStock()
        if book["stock"] == 0:
            raise OutOfStock()
        self.repo.update(isbn, {"stock": book["stock"] - 1})
        return self.repo.get(isbn)
