import uuid
from sqlalchemy import Column, String, Enum as SAEnum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.database.base import Base
from app.domain.entities.ticket import TicketStatus


class TicketModel(Base):
    __tablename__ = "tickets"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    comanda_id = Column(String, ForeignKey("orders.id"), nullable=False)
    status = Column(SAEnum(TicketStatus), nullable=False, default=TicketStatus.pendente)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    comanda = relationship("OrderModel", back_populates="tickets")
    itens = relationship("TicketItemModel", back_populates="ticket")
