import uuid
from sqlalchemy import Column, String, Enum as SAEnum
from app.infrastructure.database.base import Base
from app.domain.entities.user import UserProfile


class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    senha_hash = Column(String, nullable=False)
    perfil = Column(SAEnum(UserProfile), nullable=False)
