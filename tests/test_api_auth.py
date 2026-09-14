import jwt

from my_fastapi_project.core.config import get_settings

settings = get_settings()


def make_user_payload(
    username: str = "alice",
    email: str = "a@b.com",
    password: str = "secret123",
) -> dict:
    return {"username": username, "email": email, "password": password}


def make_login_form(
    username: str = "alice",
    password: str = "secret123",
) -> dict:
    return {"username": username, "password": password}


def test_login_returns_jwt(auth_client):
    auth_client.post("/users/register/", json=make_user_payload())

    response = auth_client.post("/token", data=make_login_form())

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"

    token = response.json()["access_token"]
    assert token.count(".") == 2

    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert payload["sub"] == "alice"


def test_login_with_wrong_password_returns_401(auth_client):
    auth_client.post("/users/register/", json=make_user_payload())

    response = auth_client.post(
        "/token",
        data=make_login_form(password="wrongpass1"),
    )

    assert response.status_code == 401
    assert response.json()["code"] == 401


def test_login_with_unknown_username_returns_401(auth_client):
    response = auth_client.post(
        "/token",
        data=make_login_form(username="nobody"),
    )

    assert response.status_code == 401


def test_login_requires_form_not_json(auth_client):
    auth_client.post("/users/register/", json=make_user_payload())

    response = auth_client.post("/token", json=make_login_form())

    assert response.status_code == 422
