from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query

from app.infrastructure.websocket.manager import manager
from dependencies import verify_token_optional

router = APIRouter()


async def _authenticate_websocket(websocket: WebSocket, token: str | None) -> bool:
    if not token:
        await websocket.close(code=1008, reason="Token obrigatorio")
        return False
    if not verify_token_optional(token):
        await websocket.close(code=1008, reason="Token invalido")
        return False
    return True


@router.websocket("/ws/kitchen")
async def websocket_kitchen(
    websocket: WebSocket,
    token: str = Query(..., description="JWT de autenticacao"),
):
    if not await _authenticate_websocket(websocket, token):
        return
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@router.websocket("/ws/notify")
async def websocket_notify(
    websocket: WebSocket,
    token: str = Query(..., description="JWT de autenticacao"),
):
    if not await _authenticate_websocket(websocket, token):
        return
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
