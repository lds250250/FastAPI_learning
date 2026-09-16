import pytest

from my_fastapi_project.repositories.book_repo import BookRepository


def make_book_data(
    isbn: str = "12345",
    title: str = "流畅的Python",
    author: str = "Luciano Ramalho",
    price: float = 139.0,
    stock: int = 5,
    internal_note: str | None = None,
) -> dict:
    return {
        "isbn": isbn,
        "title": title,
        "author": author,
        "price": price,
        "stock": stock,
        "internal_note": internal_note,
    }


@pytest.mark.anyio
async def test_create_get(empty_book_repo: BookRepository):
    await empty_book_repo.create("12345", make_book_data())
    assert (await empty_book_repo.get("12345"))["title"] == "流畅的Python"


@pytest.mark.anyio
async def test_exists(empty_book_repo: BookRepository):
    assert await empty_book_repo.exists("12345") is False
    await empty_book_repo.create("12345", make_book_data())
    assert await empty_book_repo.exists("12345") is True


@pytest.mark.anyio
async def test_list_all(empty_book_repo: BookRepository):
    await empty_book_repo.create("12345", make_book_data())
    assert await empty_book_repo.list_all() == [make_book_data()]


@pytest.mark.anyio
async def test_update(empty_book_repo: BookRepository):
    await empty_book_repo.create("12345", make_book_data())
    await empty_book_repo.update("12345", {"title": "game start"})
    assert (await empty_book_repo.get("12345"))["title"] == "game start"


@pytest.mark.anyio
async def test_delete(empty_book_repo: BookRepository):
    await empty_book_repo.create("12345", make_book_data())
    assert await empty_book_repo.delete("12345") is True
    assert await empty_book_repo.delete("12345") is False


@pytest.mark.anyio
async def test_decrement_stock_stops_at_zero(empty_book_repo: BookRepository):
    await empty_book_repo.create("12345", make_book_data(stock=1))

    assert await empty_book_repo.decrement_stock("12345") is True
    assert await empty_book_repo.decrement_stock("12345") is False
    assert (await empty_book_repo.get("12345"))["stock"] == 0
