def make_user_payload(username: str = "bob") -> dict:
    return {
        "username": username,
        "email": f"{username}@b.com",
        "password": "secret123",
    }


def register_user(client, username: str) -> None:
    response = client.post("/users/register/", json=make_user_payload(username))
    assert response.status_code == 201


def test_update_own_profile_is_allowed(auth_client):
    response = auth_client.patch("/users/caller", json={"email": "new@b.com"})

    assert response.status_code == 200


def test_update_someone_else_profile_is_forbidden(auth_client):
    register_user(auth_client, "bob")

    response = auth_client.patch("/users/bob", json={"email": "new@b.com"})

    assert response.status_code == 403


def test_admin_can_update_any_profile(admin_client):
    register_user(admin_client, "bob")

    response = admin_client.patch("/users/bob", json={"email": "new@b.com"})

    assert response.status_code == 200


def test_admin_cannot_delete_self(admin_client):
    response = admin_client.delete("/users/admin")

    assert response.status_code == 400


def test_admin_can_delete_others(admin_client):
    register_user(admin_client, "bob")

    response = admin_client.delete("/users/bob")

    assert response.status_code == 204
