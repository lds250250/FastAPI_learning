def test_echo_returns_same_message(client):
    with client.websocket_connect("/ws") as ws:
        ws.send_text("你好")
        assert ws.receive_text() == "你说了：你好"


def test_one_connection_can_send_multiple_messages(client):
    with client.websocket_connect("/ws") as ws:
        for word in ["一", "二", "三"]:
            ws.send_text(word)
            assert ws.receive_text() == f"你说了：{word}"
