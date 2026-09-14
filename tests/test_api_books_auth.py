def test_list_books_returns_empty_list(auth_client):
    response = auth_client.get("/books/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_book(auth_client):
    response = auth_client.post(
        "/books/",
        json={
            "isbn": "9787115428028",
            "title": "流畅的Python",
            "author": "Luciano Ramalho",
            "price": 139.0,
            "stock": 5,
        },
    )
    assert response.status_code == 201
    assert response.json()["isbn"] == "9787115428028"
    assert "internal_note" not in response.json()


def test_create_duplicate_isbn_returns_409(auth_client):
    book = {
        "isbn": "9787115428028",
        "title": "流畅的Python",
        "author": "Luciano Ramalho",
        "price": 139.0,
        "stock": 5,
    }
    assert auth_client.post("/books/", json=book).status_code == 201

    response = auth_client.post("/books/", json=book)
    assert response.status_code == 409
    assert response.json()["code"] == 409


def test_delete_book_requires_admin(auth_client):
    book = {
        "isbn": "9787115428028",
        "title": "流畅的Python",
        "author": "Luciano Ramalho",
        "price": 139.0,
        "stock": 5,
    }
    auth_client.post("/books/", json=book)

    response = auth_client.delete("/books/9787115428028")
    assert response.status_code == 403


def test_delete_book_as_admin(admin_client):
    book = {
        "isbn": "9787115428028",
        "title": "流畅的Python",
        "author": "Luciano Ramalho",
        "price": 139.0,
        "stock": 5,
    }
    admin_client.post("/books/", json=book)

    response = admin_client.delete("/books/9787115428028")
    assert response.status_code == 204
