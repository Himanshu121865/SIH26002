from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from api.routes_routing import router as routing_router
from api.routes_tracking import router as tracking_router
from api.routes_alerts import router as alerts_router
from api.routes_reports import router as reports_router

router = APIRouter()
router.include_router(routing_router, prefix="/routing", tags=["routing"])
router.include_router(tracking_router, prefix="/tracking", tags=["tracking"])
router.include_router(alerts_router, prefix="/alerts", tags=["alerts"])
router.include_router(reports_router, prefix="/reports", tags=["reports"])


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)


manager = ConnectionManager()
