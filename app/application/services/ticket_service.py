from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.domain.entities.order import OrderStatus
from app.domain.entities.ticket import TicketStatus
from app.infrastructure.database.models.order_model import OrderModel
from app.infrastructure.database.models.ticket_model import TicketModel


def mark_ticket_ready(db: Session, ticket_id: str) -> TicketModel:
    ticket = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket nao encontrado")

    order = db.query(OrderModel).filter(OrderModel.id == ticket.comanda_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comanda nao encontrada")

    if order.status != OrderStatus.aberta:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Comanda fechada; ticket nao pode ser alterado",
        )

    if ticket.status == TicketStatus.pronto:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ticket ja esta pronto",
        )

    ticket.status = TicketStatus.pronto
    db.commit()
    db.refresh(ticket)
    return ticket
