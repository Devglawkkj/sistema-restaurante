import uuid
from sqlalchemy import Column, String, Float, Enum as SAEnum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.database.base import Base
from app.domain.entities.payment import PaymentMethod


class PaymentModel(Base):
    __tablename__ = "payments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    comanda_id = Column(String, ForeignKey("orders.id"), nullable=False)
    valor = Column(Float, nullable=False)
    metodo = Column(SAEnum(PaymentMethod), nullable=False)
    data_pagamento = Column(DateTime(timezone=True), server_default=func.now())

    comanda = relationship("OrderModel", back_populates="pagamento")
