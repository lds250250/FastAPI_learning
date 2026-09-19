import logging
import uuid
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect

from my_fastapi_project.api import ws_bus
from my_fastapi_project.api.deps import (
    ManagerDep,
    RedisDep,
    UserServiceDep,
    require_role,
)
from my_fastapi_project.core.logging_config import request_id_var
from my_fastapi_project.core.roles import ROLE_ADMIN
from my_fastapi_project.core.security import decode_access_token

router = APIRouter(tags=["ws"])
logger = logging.getLogger(__name__)

WS_UNAUTHORIZED = 4001


async def _authenticate(token: str | None, service) -> dict | None:
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
    request_id_var.set(f"ws-{uuid.uuid4().hex[:8]}")
    await manager.connect(username, websocket)

    logger.info("WebSocket 连接建立：%s", username)

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
        logger.info("WebSocket 连接断开：%s", username)


@router.post(
    "/ws/announce",
    status_code=204,
    dependencies=[Depends(require_role(ROLE_ADMIN))],
)
async def announce(cache: RedisDep, message: Annotated[str, Query(min_length=1)]):
    await ws_bus.publish(cache, f"【公告】{message}")
