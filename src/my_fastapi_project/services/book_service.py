from typing import Any

from my_fastapi_project.repositories.book_repo import BookRepository
from my_fastapi_project.schemas.book import BookCreate, BookUpdate


class BookService:
    def __init__(self, repo: BookRepository):
        self.repo = repo

    def create(self, book: BookCreate) -> dict[str, Any] | None:
        if self.repo.exists(book.isbn):
            return None
        data = book.model_dump()
        return self.repo.create(book.isbn, data)

    def list_book(self, offset: int, limit: int) -> list[dict[str, Any]]:
        books = self.repo.list_all()
        return books[offset: offset + limit]

    def get_book(self, isbn: str) -> dict[str, Any] | None:
        return self.repo.get(isbn)

    def update_book(self, isbn: str, data: BookUpdate) -> dict[str, Any] | None:
        payload = data.model_dump(exclude_unset=True)
        return self.repo.update(isbn, payload)

    def delete_book(self, isbn: str) -> bool:
        return self.repo.delete(isbn)

    def borrow(self, isbn: str) -> dict[str, Any] | None:
        book = self.repo.get(isbn)
        if book is None or book["stock"] == 0:
            return None
        self.repo.update(isbn, {"stock": book["stock"]-1})
        return self.repo.get(isbn)
