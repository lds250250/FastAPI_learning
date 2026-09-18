import asyncio

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


def test_message_is_broadcast_to_sender(client, ws_token):
    with client.websocket_connect(f"/ws?token={ws_token}") as ws:
        assert ws.receive_text() == "欢迎，wsuser"

        ws.send_text("你好")
        assert ws.receive_text() == "wsuser 说：你好"


def test_one_connection_can_send_multiple_messages(client, ws_token):
    with client.websocket_connect(f"/ws?token={ws_token}") as ws:
        ws.receive_text()

        for word in ["一", "二", "三"]:
            ws.send_text(word)
            assert ws.receive_text() == f"wsuser 说：{word}"


def test_message_is_broadcast_to_other_connections(client, ws_token):
    with client.websocket_connect(f"/ws?token={ws_token}") as first:
        first.receive_text()

        with client.websocket_connect(f"/ws?token={ws_token}") as second:
            second.receive_text()

            first.send_text("大家好")

            assert first.receive_text() == "wsuser 说：大家好"
            assert second.receive_text() == "wsuser 说：大家好"


def test_direct_message_only_reaches_the_target(client, ws_token, bob_token):
    with client.websocket_connect(f"/ws?token={ws_token}") as alice:
        alice.receive_text()

        with client.websocket_connect(f"/ws?token={bob_token}") as bob:
            bob.receive_text()

            alice.send_text("/msg bob 悄悄话")

            assert bob.receive_text() == "wsuser 悄悄说：悄悄话"
            assert alice.receive_text() == "已发给 bob"


def test_broadcast_drops_the_dead_connection(client, ws_token, ws_manager):
    asyncio.run(ws_manager.connect("ghost", _DeadSocket()))

    with client.websocket_connect(f"/ws?token={ws_token}") as ws:
        ws.receive_text()

        ws.send_text("还在吗")

        assert ws.receive_text() == "wsuser 说：还在吗"

    assert not ws_manager.is_online("ghost")


class _DeadSocket:
    async def accept(self) -> None:
        pass

    async def send_text(self, message: str) -> None:
        raise RuntimeError("这条连接已经死了")


def test_announce_reaches_connected_clients(client, ws_token, admin_token):
    with client.websocket_connect(f"/ws?token={ws_token}") as ws:
        ws.receive_text()

        response = client.post(
            "/ws/announce",
            params={"message": "系统维护通知"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert response.status_code == 204
        assert ws.receive_text() == "【公告】系统维护通知"


def test_announce_requires_admin(client, ws_token):
    response = client.post(
        "/ws/announce",
        params={"message": "我不是管理员"},
        headers={"Authorization": f"Bearer {ws_token}"},
    )

    assert response.status_code == 403
