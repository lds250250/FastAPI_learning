API_KEY_HEADERS = {"x-api-key": "demo-secret-key"}


def test_list_books_without_key_returns_401(client):
    response = client.get("/books/")
    assert response.status_code == 401
    assert response.json()["code"] == 401


def test_list_books_with_key(client):
    response = client.get("/books/", headers=API_KEY_HEADERS)
    assert response.status_code == 200
    assert response.json() == []


def test_get_missing_book_returns_404(auth_client):
    response = auth_client.get("/books/0000000000000")
    assert response.status_code == 404
    assert "0000000000000" in response.json()["message"]


def test_create_book_with_invalid_price(auth_client):
    response = auth_client.post(
        "/books/",
        json={
            "isbn": "9787115428028",
            "title": "流畅的Python",
            "author": "Luciano Ramalho",
            "price": -1,
            "stock": 5,
        },
    )
    assert response.status_code == 422
    assert response.json()["code"] == 422


def test_rate_limit_blocks_sixth_request(auth_client):
    for _ in range(5):
        response = auth_client.get("/books/")
        assert response.status_code == 200

    response = auth_client.get("/books/")

    assert response.status_code == 429
    assert response.json()["code"] == 429
