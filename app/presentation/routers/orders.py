from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.infrastructure.database.connection import get_db
from app.application.services import order_service
from app.infrastructure.websocket.manager import manager
from app.presentation.schemas.ticket_schema import TicketCreate, OrderDetailResponse, BillResponse
from app.presentation.schemas.order_schema import OrderResponse
from dependencies import get_current_user

router = APIRouter()


@router.get("/table/{table_id}/active", response_model=OrderDetailResponse)
def get_active_order_for_table(
    table_id: str,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    order = order_service.get_active_order_for_table(db, table_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhuma comanda aberta nesta mesa",
        )
    return order_service.get_order_detail(db, order.id)


@router.get("/{order_id}", response_model=OrderDetailResponse)
def get_order(
    order_id: str,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    return order_service.get_order_detail(db, order_id)


@router.post("/{order_id}/tickets", response_model=OrderDetailResponse, status_code=201)
async def add_ticket(
    order_id: str,
    data: TicketCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    ticket = order_service.add_ticket(db, order_id, data)
    detail = order_service.get_order_detail(db, order_id)
    await manager.broadcast({
        "evento": "novo_ticket",
        "ticket_id": ticket.id,
        "comanda_id": order_id,
        "mesa_numero": detail.get("mesa_numero"),
    })
    return detail


@router.get("/{order_id}/bill", response_model=BillResponse)
def get_bill(
    order_id: str,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    return order_service.get_order_bill(db, order_id)


@router.post("/{order_id}/close", response_model=OrderResponse)
def close_order(
    order_id: str,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    return order_service.close_order(db, order_id)


@router.post("/table/{table_id}", response_model=OrderResponse, status_code=201)
def create_or_get_order(
    table_id: str,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    return order_service.get_or_create_order(db, table_id)