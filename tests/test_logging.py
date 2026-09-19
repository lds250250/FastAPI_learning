import logging

import pytest

from my_fastapi_project.core.logging_config import RedactingFormatter
from my_fastapi_project.repositories.user_repo import UserRepository


def test_request_is_logged(client, caplog):
    with caplog.at_level(logging.INFO):
        client.get("/health")

    messages = [record.getMessage() for record in caplog.records]

    assert any("/health" in message for message in messages)


def test_redacting_formatter_hides_token():
    formatter = RedactingFormatter("%(message)s")
    record = logging.LogRecord(
        name="demo",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="连上来了：%s",
        args=("ws://127.0.0.1:8000/ws?token=secret-abc",),
        exc_info=None,
    )

    output = formatter.format(record)

    assert "secret-abc" not in output
    assert "token=***" in output


def test_request_id_is_attached_to_every_log_of_a_request(client, caplog):
    with caplog.at_level(logging.INFO):
        client.get("/health", headers={"x-request-id": "trace-abc"})

    records = [r for r in caplog.records if r.name.startswith("my_fastapi_project")]

    assert len(records) >= 2
    assert all(r.request_id == "trace-abc" for r in records)


def test_websocket_connection_is_logged(client, ws_token, caplog):
    with caplog.at_level(logging.INFO):
        with client.websocket_connect(f"/ws?token={ws_token}"):
            pass

    messages = [r.getMessage() for r in caplog.records]

    assert any("连接建立" in m for m in messages)
    assert any("连接断开" in m for m in messages)


def test_unhandled_exception_is_logged(auth_client, caplog, monkeypatch):
    async def boom(self, *args, **kwargs):
        raise RuntimeError("模拟意外崩溃")

    monkeypatch.setattr(UserRepository, "list_all", boom)

    with caplog.at_level(logging.ERROR):
        with pytest.raises(RuntimeError):
            auth_client.get("/users/")

    messages = [r.getMessage() for r in caplog.records]

    assert any("未处理的异常" in m for m in messages)


def test_borrow_is_logged(auth_client, sample_book, caplog):
    with caplog.at_level(logging.INFO):
        auth_client.post(f"/books/{sample_book}/borrow")

    messages = [r.getMessage() for r in caplog.records]

    assert any("借阅成功" in m for m in messages)
