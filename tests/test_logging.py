import logging

from my_fastapi_project.core.logging_config import RedactingFormatter


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
