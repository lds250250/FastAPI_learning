def test_full_auth_flow(client):

    register = client.post(
        "/users/register/",
        json={"username": "alice", "email": "a@b.com", "password": "secret123"},
    )
    assert register.status_code == 201

    login = client.post(
        "/token",
        data={"username": "alice", "password": "secret123"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]

    me = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["username"] == "alice"

    refreshed = client.post(
        "/token/refresh",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert refreshed.status_code == 200
    new_token = refreshed.json()["access_token"]

    me_again = client.get("/users/me", headers={"Authorization": f"Bearer {new_token}"})
    assert me_again.status_code == 200

    assert me_again.json()["username"] == "alice"
