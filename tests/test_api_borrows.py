def test_my_borrows_lists_borrowed_books(auth_client, sample_book):
    auth_client.post(f"/books/{sample_book}/borrow")

    response = auth_client.get("/borrows/me")

    assert response.status_code == 200
    records = response.json()
    assert len(records) == 1
    assert records[0]["isbn"] == sample_book
    assert records[0]["title"] == "流畅的Python"
    assert records[0]["returned_at"] is None


def test_my_borrows_is_empty_for_new_user(auth_client):
    response = auth_client.get("/borrows/me")

    assert response.status_code == 200
    assert response.json() == []


def test_my_borrows_requires_login(client):
    response = client.get("/borrows/me")

    assert response.status_code == 401
