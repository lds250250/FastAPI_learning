def make_user_payload(
    username: str = "alice",
    email: str = "a@b.com",
    password: str = "secret123",
) -> dict:
    return {"username": username, "email": email, "password": password}


def test_register_user(auth_client):
    response = auth_client.post("/users/register/", json=make_user_payload())

    assert response.status_code == 201
    assert response.json()["username"] == "alice"
    assert "password" not in response.json()


def test_register_duplicate_username_returns_409(auth_client):
    auth_client.post("/users/register/", json=make_user_payload())

    response = auth_client.post(
        "/users/register/",
        json=make_user_payload(email="other@b.com"),
    )

    assert response.status_code == 409
    assert response.json()["code"] == 409


def test_get_user(auth_client):
    auth_client.post("/users/register/", json=make_user_payload())

    response = auth_client.get("/users/alice")

    assert response.status_code == 200
    assert response.json()["username"] == "alice"


def test_get_missing_user_returns_404(auth_client):
    response = auth_client.get("/users/nobody")

    assert response.status_code == 404
    assert "nobody" in response.json()["message"]


def test_list_users_with_pagination(auth_client):
    auth_client.post("/users/register/", json=make_user_payload())
    auth_client.post(
        "/users/register/",
        json=make_user_payload(username="bob", email="b@b.com"),
    )

    response = auth_client.get("/users/?page=1&size=1")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_delete_user_requires_admin(auth_client):
    auth_client.post("/users/register/", json=make_user_payload())

    response = auth_client.delete("/users/alice")

    assert response.status_code == 403


def test_delete_user_as_admin(admin_client):
    admin_client.post("/users/register/", json=make_user_payload())

    response = admin_client.delete("/users/alice")

    assert response.status_code == 204


def test_register_password_over_72_bytes_returns_422(auth_client):
    response = auth_client.post(
        "/users/register/",
        json=make_user_payload(password="中" * 25),
    )

    assert response.status_code == 422
