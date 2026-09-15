import time

import jwt
import pytest

from my_fastapi_project.core.config import get_settings
from my_fastapi_project.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)

settings = get_settings()


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


def test_access_token_carries_subject():
    token = create_access_token("alice")

    payload = decode_access_token(token)

    assert payload["sub"] == "alice"


def test_access_token_expires_in_the_future():
    token = create_access_token("alice")

    payload = decode_access_token(token)

    assert payload["exp"] > time.time()


def test_token_signed_with_another_key_is_rejected():
    forged = jwt.encode(
        {"sub": "alice", "exp": time.time() + 3600},
        "wrong-secret-wrong-secret-wrong-secret",
        algorithm="HS256",
    )

    with pytest.raises(jwt.InvalidTokenError):
        decode_access_token(forged)


def text_expired_token_is_rejected():
    token = create_access_token("alice", expires_minutes=-1)

    with pytest.raises(jwt.ExpiredSignatureError):
        decode_access_token(token)


def test_expires_minutes_is_respected():
    token = create_access_token("alice", expires_minutes=1)

    payload = decode_access_token(token)

    remaining_seconds = payload["exp"] - time.time()
    assert 0 < remaining_seconds <= 60


def test_expired_token_is_rejected():
    token = create_access_token("alice", expires_minutes=-1)

    with pytest.raises(jwt.ExpiredSignatureError):
        decode_access_token(token)
