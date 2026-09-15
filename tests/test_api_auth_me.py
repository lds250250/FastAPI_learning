import time

import jwt

from my_fastapi_project.core.security import create_access_token


def register_user(client, username: str = "alice") -> str:
    client.post(
        "/users/register/",
        json={
            "username": username,
            "email": f"{username}@b.com",
            "password": "secret123",
        },
    )
    response = client.post(
        "/token",
        data={"username": username, "password": "secret123"},
    )
    return response.json()["access_token"]


def test_me_returns_caller(client):
    token = register_user(client)

    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json()["username"] == "alice"


def test_me_without_token_returns_401(client):
    response = client.get("/users/me")

    assert response.status_code == 401


def test_me_with_garbage_token_returns_401(client):
    response = client.get("/users/me", headers={"Authorization": "Bearer not-a-jwt"})

    assert response.status_code == 401


def test_me_with_forged_token_returns_401(client):
    forged = jwt.encode(
        {"sub": "alice", "exp": time.time() + 3600},
        "wrong-secret-wrong-secret-wrong-secret",
        algorithm="HS256",
    )

    response = client.get("/users/me", headers={"Authorization": f"Bearer {forged}"})

    assert response.status_code == 401


def test_me_with_expired_token_returns_401(client):
    register_user(client)

    expired = create_access_token("alice", expires_minutes=-1)

    response = client.get("/users/me", headers={"Authorization": f"Bearer {expired}"})

    assert response.status_code == 401


def test_refresh_returns_a_new_token(auth_client):
    response = auth_client.post("/token/refresh")

    assert response.status_code == 200
    assert response.json()["access_token"]


def test_refresh_without_token_returns_401(client):
    response = client.post("/token/refresh")

    assert response.status_code == 401
