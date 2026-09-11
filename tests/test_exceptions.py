from my_fastapi_project.core.exceptions import (
    EmailAlreadyExists,
    OutOfStock,
    UsernameAlreadyExists,
)


def test_username_already_exists_carries_409():
    exc = UsernameAlreadyExists("alice")
    assert exc.status_code == 409
    assert exc.message == "用户名'alice'已存在"


def test_email_already_exists_message_contains_the_email():
    exc = EmailAlreadyExists("a@b.com")
    assert exc.status_code == 409
    assert "a@b.com" in exc.message


def test_out_of_stock_carries_400():
    exc = OutOfStock()
    assert exc.status_code == 400
