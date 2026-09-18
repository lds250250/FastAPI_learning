from fastapi import WebSocket, WebSocketDisconnect


class ConnectionManager:
    def __init__(self) -> None:
        self._connections: dict[str, list[WebSocket]] = {}

    async def connect(self, username: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self._connections.setdefault(username, []).append(websocket)

    async def send_to_user(self, username: str, message: str) -> None:
        for websocket in list(self._connections.get(username, [])):
            await self._safe_send(username, websocket, message)

    async def broadcast_local(self, message: str) -> None:
        for username, sockets in list(self._connections.items()):
            for websocket in list(sockets):
                await self._safe_send(username, websocket, message)

    async def _safe_send(
        self, username: str, websocket: WebSocket, message: str
    ) -> None:
        try:
            await websocket.send_text(message)
        except (WebSocketDisconnect, RuntimeError):
            self.disconnect(username, websocket)

    def disconnect(self, username: str, websocket: WebSocket) -> None:
        sockets = self._connections.get(username)

        if not sockets or websocket not in sockets:
            return

        sockets.remove(websocket)

        if not sockets:
            del self._connections[username]

    def is_online(self, username: str) -> bool:
        return username in self._connections

    def connection_count(self, username: str) -> int:
        return len(self._connections.get(username, []))

    def online_users(self) -> list[str]:
        return list(self._connections)


manager = ConnectionManager()
