from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infrastructure.database.connection import get_db
from app.application.services import kitchen_service
from app.application.services import ticket_service
from app.infrastructure.websocket.manager import manager
from dependencies import get_current_user

router = APIRouter()


@router.get("/tickets")
def list_pending_tickets(
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    return kitchen_service.get_pending_tickets(db)


@router.patch("/tickets/{ticket_id}/ready")
async def mark_ready(
    ticket_id: str,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    ticket = ticket_service.mark_ticket_ready(db, ticket_id)

    await manager.broadcast({
        "evento": "ticket_pronto",
        "ticket_id": ticket.id,
        "comanda_id": ticket.comanda_id,
    })

    return {"message": "Ticket marcado como pronto", "ticket_id": ticket.id}