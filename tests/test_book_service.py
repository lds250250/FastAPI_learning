"""
create 成功创建，返回值字段正确
create 重复 ISBN → 抛 BookAlreadyExists
borrow 成功：返回的书里 stock 减了 1
borrow 库存为 0 → 抛 OutOfStock
get_book 查不到 → 返回 None
list_book(offset, limit) 切片正确
"""

import pytest

from my_fastapi_project.core.exceptions import BookAlreadyExists, OutOfStock
from my_fastapi_project.schemas.book import BookCreate
from my_fastapi_project.services.book_service import BookRepository, BookService


@pytest.fixture
def service() -> BookService:
    return BookService(BookRepository())


def make_book(
    isbn: str = "9787115428028",
    title: str = "流畅的Python",
    author: str = "Luciano Ramalho",
    price: float = 139.0,
    stock: int = 5,
) -> BookCreate:
    return BookCreate(isbn=isbn, title=title, author=author, price=price, stock=stock)


def test_register_repeat_book_raises(service):
    service.create(make_book())

    with pytest.raises(BookAlreadyExists):
        service.create(make_book(isbn="9787115428028"))


def test_register_borrow_is_right(service):
    service.create(make_book())

    result = service.borrow("9787115428028")

    assert result["stock"] == 4


def test_register_borrow_zero_raises(service):
    service.create(make_book(stock=0))

    with pytest.raises(OutOfStock):
        service.borrow(make_book(isbn="9787115428028"))


def test_register_get_book_none(service):
    service.create(make_book())
    assert service.get_book("0000000000000") is None


def test_register_list_book(service):
    book = service.create(make_book())
    assert service.list_book(0, 5) == [book]
