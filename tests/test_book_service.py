import pytest

from my_fastapi_project.core.exceptions import BookAlreadyExists, OutOfStock
from my_fastapi_project.repositories.book_repo import BookRepository
from my_fastapi_project.repositories.borrow_repo import BorrowRecordRepository
from my_fastapi_project.schemas.book import BookCreate
from my_fastapi_project.services.book_service import BookService


@pytest.fixture
async def service(db_factory, fake_redis):
    async with db_factory() as session:
        yield BookService(
            BookRepository(session),
            BorrowRecordRepository(session),
            fake_redis,
        )


def make_book(
    isbn: str = "9787115428028",
    title: str = "流畅的Python",
    author: str = "Luciano Ramalho",
    price: float = 139.0,
    stock: int = 5,
) -> BookCreate:
    return BookCreate(isbn=isbn, title=title, author=author, price=price, stock=stock)


@pytest.mark.anyio
async def test_register_repeat_book_raises(service):
    await service.create(make_book())

    with pytest.raises(BookAlreadyExists):
        await service.create(make_book("9787115428028"))


@pytest.mark.anyio
async def test_register_borrow_is_right(service, alice):
    await service.create(make_book())

    result = await service.borrow(alice, "9787115428028")

    assert result["stock"] == 4


@pytest.mark.anyio
async def test_register_borrow_zero_raises(service, alice):
    await service.create(make_book(stock=0))

    with pytest.raises(OutOfStock):
        await service.borrow(alice, "9787115428028")


@pytest.mark.anyio
async def test_register_get_book_none(service):
    await service.create(make_book())
    assert await service.get_book("0000000000000") is None


@pytest.mark.anyio
async def test_register_list_book(service):
    book = await service.create(make_book())
    assert await service.list_book(0, 5) == [book]
