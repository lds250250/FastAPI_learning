from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(tags=["ws"])


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            text = await websocket.receive_text()
            await websocket.send_text(f"你说了：{text}")
    except WebSocketDisconnect:
        pass
