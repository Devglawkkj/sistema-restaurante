import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.domain.entities.order import OrderStatus
from app.infrastructure.database.models.payment_model import PaymentModel
from app.application.services.order_service import _get_order, calculate_order_total
from app.presentation.schemas.payment_schema import PaymentCreate


def create_payment(db: Session, order_id: str, data: PaymentCreate) -> PaymentModel:
    order = _get_order(db, order_id)
    if order.status != OrderStatus.aberta:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Comanda ja foi fechada",
        )

    existing = db.query(PaymentModel).filter(PaymentModel.comanda_id == order_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Pagamento ja registrado para esta comanda",
        )

    expected_total = round(calculate_order_total(db, order_id), 2)
    valor_informado = round(data.valor, 2)
    if expected_total <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Comanda sem itens para pagamento",
        )
    if abs(valor_informado - expected_total) > 0.01:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Valor informado ({valor_informado:.2f}) difere do total ({expected_total:.2f})",
        )

    payment = PaymentModel(
        id=str(uuid.uuid4()),
        comanda_id=order_id,
        valor=valor_informado,
        metodo=data.metodo,
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment
