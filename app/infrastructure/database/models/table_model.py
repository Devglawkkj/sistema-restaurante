import uuid
from sqlalchemy import Column, String, Integer, Enum as SAEnum
from app.infrastructure.database.base import Base
from app.domain.entities.table import TableStatus


class TableModel(Base):
    __tablename__ = "tables"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    numero = Column(Integer, unique=True, nullable=False)
    status = Column(SAEnum(TableStatus), nullable=False, default=TableStatus.livre)
