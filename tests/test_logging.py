import logging


def test_request_is_logged(client, caplog):
    with caplog.at_level(logging.INFO):
        client.get("/health")

    messages = [record.getMessage() for record in caplog.records]

    assert any("/health" in message for message in messages)
