from my_fastapi_project.core.security import hash_password, verify_password


def test_hash_does_not_contain_the_plain_password():
    hashed = hash_password("secret123")

    assert hashed != "secret123"
    assert "secret123" not in hashed


def test_same_password_hashes_differently():
    first = hash_password("secret123")
    second = hash_password("secret123")

    assert first != second


def test_verify_accepts_correct_password():
    hashed = hash_password("secret123")

    assert verify_password("secret123", hashed) is True


def test_verify_rejects_wrong_password():
    hashed = hash_password("secret123")

    assert verify_password("wrongpass1", hashed) is False
