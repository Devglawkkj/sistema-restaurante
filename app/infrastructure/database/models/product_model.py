import uuid
from sqlalchemy import Column, String, Float, Boolean
from app.infrastructure.database.base import Base


class ProductModel(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    categoria = Column(String, nullable=False)
    ativo = Column(Boolean, default=True, nullable=False)
