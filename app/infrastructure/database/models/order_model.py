import uuid
from sqlalchemy import Column, String, Enum as SAEnum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.database.base import Base
from app.domain.entities.order import OrderStatus


class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    mesa_id = Column(String, ForeignKey("tables.id"), nullable=False)
    status = Column(SAEnum(OrderStatus), nullable=False, default=OrderStatus.aberta)
    data_abertura = Column(DateTime(timezone=True), server_default=func.now())
    data_fechamento = Column(DateTime(timezone=True), nullable=True)

    mesa = relationship("TableModel")
    tickets = relationship("TicketModel", back_populates="comanda")
    pagamento = relationship("PaymentModel", back_populates="comanda", uselist=False)
