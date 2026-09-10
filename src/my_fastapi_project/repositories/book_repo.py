from typing import Any

_books: dict[str, dict[str, Any]] = {}

# get(isbn) list_all()  update(isbn, data) delete(isbn) create(isbn, data) exists(isbn)


class BookRepository:
    def create(self, isbn: str, data: dict) -> dict[str, Any]:
        _books[isbn] = data
        return data

    def exists(self, isbn: str) -> bool:
        return isbn in _books

    def get(self, isbn: str) -> dict[str, Any] | None:
        return _books.get(isbn)

    def list_all(self) -> list[dict[str, Any]]:
        return list(_books.values())

    def update(self, isbn: str, data: dict) -> dict[str, Any] | None:
        book = _books.get(isbn)
        if book is None:
            return None
        book.update(data)
        return book

    def delete(self, isbn: str) -> bool:
        return _books.pop(isbn, None) is not None
