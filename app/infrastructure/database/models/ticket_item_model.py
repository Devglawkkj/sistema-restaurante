import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.infrastructure.database.base import Base


class TicketItemModel(Base):
    __tablename__ = "ticket_items"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    ticket_id = Column(String, ForeignKey("tickets.id"), nullable=False)
    produto_id = Column(String, ForeignKey("products.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    observacao = Column(Text, nullable=True)

    ticket = relationship("TicketModel", back_populates="itens")
    produto = relationship("ProductModel")
