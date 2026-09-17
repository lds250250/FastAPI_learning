def make_book_payload(
    isbn: str = "9787115428028",
    title: str = "流畅的Python",
    author: str = "Luciano Ramalho",
    price: float = 139.0,
    stock: int = 5,
) -> dict:
    return {
        "isbn": isbn,
        "title": title,
        "author": author,
        "price": price,
        "stock": stock,
    }


def test_list_books_returns_empty_list(auth_client):
    response = auth_client.get("/books/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_book(admin_client):
    response = admin_client.post("/books/", json=make_book_payload())

    assert response.status_code == 201
    assert response.json()["isbn"] == "9787115428028"
    assert "internal_note" not in response.json()


def test_create_duplicate_isbn_returns_409(admin_client):
    assert admin_client.post("/books/", json=make_book_payload()).status_code == 201
    response = admin_client.post("/books/", json=make_book_payload())

    assert response.status_code == 409
    assert response.json()["code"] == 409


def test_delete_book_requires_admin(auth_client, sample_book):
    response = auth_client.delete(f"/books/{sample_book}")

    assert response.status_code == 403


def test_delete_book_as_admin(admin_client):
    admin_client.post("/books/", json=make_book_payload())
    response = admin_client.delete("/books/9787115428028")

    assert response.status_code == 204


def test_borrow_then_return(auth_client, sample_book):
    borrowed = auth_client.post(f"/books/{sample_book}/borrow")
    assert borrowed.status_code == 200
    assert borrowed.json()["stock"] == 4

    returned = auth_client.post(f"/books/{sample_book}/return")
    assert returned.status_code == 200
    assert returned.json()["stock"] == 5


def test_return_without_borrowing_returns_400(auth_client, sample_book):
    response = auth_client.post(f"/books/{sample_book}/return")

    assert response.status_code == 400
    assert response.json()["code"] == 400


def test_borrowed_book_stock_is_not_stale(auth_client, sample_book):
    assert auth_client.get(f"/books/{sample_book}").json()["stock"] == 5

    auth_client.post(f"/books/{sample_book}/borrow")

    assert auth_client.get(f"/books/{sample_book}").json()["stock"] == 4


def test_updated_book_title_is_not_stale(admin_client, sample_book):
    assert admin_client.get(f"/books/{sample_book}").json()["title"] == "流畅的Python"

    admin_client.patch(f"/books/{sample_book}", json={"title": "新的书名"})

    assert admin_client.get(f"/books/{sample_book}").json()["title"] == "新的书名"
