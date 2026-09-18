import pytest
from starlette.websockets import WebSocketDisconnect

from my_fastapi_project.api.routers.ws import WS_UNAUTHORIZED


def test_connection_is_rejected_without_token(client):
    with pytest.raises(WebSocketDisconnect) as exc:
        with client.websocket_connect("/ws"):
            pass

    assert exc.value.code == WS_UNAUTHORIZED


def test_connection_is_rejected_with_invalid_token(client):
    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect("/ws?token=not-a-jwt"):
            pass


def test_valid_token_is_accepted_and_echo_works(client, ws_token):
    with client.websocket_connect(f"/ws?token={ws_token}") as ws:
        assert ws.receive_text() == "欢迎，wsuser"

        ws.send_text("你好")
        assert ws.receive_text() == "你说了：你好"


def test_one_connection_can_send_multiple_messages(client, ws_token):
    with client.websocket_connect(f"/ws?token={ws_token}") as ws:
        ws.receive_text()

        for word in ["一", "二", "三"]:
            ws.send_text(word)
            assert ws.receive_text() == f"你说了：{word}"
