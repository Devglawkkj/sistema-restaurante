# Pagamentos: um registro por comanda; exige valor igual ao total calculado dos tickets.
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infrastructure.database.connection import get_db
from app.application.services import payment_service
from app.presentation.schemas.payment_schema import PaymentCreate, PaymentResponse
from dependencies import get_current_user

router = APIRouter()


@router.post("/{order_id}", response_model=PaymentResponse, status_code=201)
def register_payment(
    order_id: str,
    data: PaymentCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    return payment_service.create_payment(db, order_id, data)
