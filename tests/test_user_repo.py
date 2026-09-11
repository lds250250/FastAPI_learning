def test_create_then_get(empty_user_repo):
    empty_user_repo.create("alice", {"username": "alice", "email": "a@b.com"})
    assert empty_user_repo.get("alice")["email"] == "a@b.com"


def test_get_missing_returns_none(empty_user_repo):
    assert empty_user_repo.get("nobody") is None


def test_exists(empty_user_repo):
    assert empty_user_repo.exists("alice") is False
    empty_user_repo.create("alice", {"username": "alice"})
    assert empty_user_repo.exists("alice") is True


def test_update(empty_user_repo):
    empty_user_repo.create("alice", {"username": "alice", "email": "a@b.com"})
    empty_user_repo.update("alice", {"email": "new@b.com"})
    assert empty_user_repo.get("alice")["email"] == "new@b.com"


def test_delete(empty_user_repo):
    empty_user_repo.create("alice", {"username": "alice"})
    assert empty_user_repo.delete("alice") is True
    assert empty_user_repo.delete("alice") is False


def test_a_creates_alice(empty_user_repo):
    empty_user_repo.create("alice", {"username": "alice"})
    assert empty_user_repo.exists("alice") is True


def test_b_starts_empty(empty_user_repo):
    assert empty_user_repo.exists("alice") is False
