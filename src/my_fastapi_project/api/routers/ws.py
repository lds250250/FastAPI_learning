from typing import Annotated

import jwt
from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect

from my_fastapi_project.api import ws_bus
from my_fastapi_project.api.deps import ManagerDep, RedisDep, UserServiceDep
from my_fastapi_project.core.security import decode_access_token

router = APIRouter(tags=["ws"])

WS_UNAUTHORIZED = 4001


async def _authenticate(token: str | None, service) -> dict | None:
    """从令牌解出调用者。任何一步不成立都返回 None，不抛异常。"""
    if not token:
        return None

    try:
        payload = decode_access_token(token)
    except jwt.InvalidTokenError:
        return None

    return await service.get_user(payload["sub"])


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    service: UserServiceDep,
    manager: ManagerDep,
    cache: RedisDep,
    token: Annotated[str | None, Query()] = None,
):
    caller = await _authenticate(token, service)

    if caller is None:
        await websocket.close(code=WS_UNAUTHORIZED)
        return

    username = caller["username"]
    await manager.connect(username, websocket)

    try:
        await websocket.send_text(f"欢迎，{username}")

        while True:
            text = await websocket.receive_text()

            if text.startswith("/msg "):
                parts = text.split(" ", 2)

                if len(parts) != 3:
                    await websocket.send_text("用法：/msg 用户名 内容")
                    continue

                _, target, content = parts
                await manager.send_to_user(target, f"{username} 悄悄说：{content}")
                await websocket.send_text(f"已发给 {target}")
                continue

            await ws_bus.publish(cache, f"{username} 说：{text}")

    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect(username, websocket)
