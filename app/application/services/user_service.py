import uuid
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.infrastructure.database.models.user_model import UserModel
from app.presentation.schemas.user_schema import UserCreate, UserUpdate
from app.application.services.auth_service import hash_password


def get_all_users(db: Session):
    return db.query(UserModel).all()


def get_user_by_id(db: Session, user_id: str) -> UserModel:
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario nao encontrado")
    return user


def create_user(db: Session, data: UserCreate) -> UserModel:
    existing = db.query(UserModel).filter(UserModel.email == data.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email ja cadastrado")
    user = UserModel(
        id=str(uuid.uuid4()),
        nome=data.nome,
        email=data.email,
        senha_hash=hash_password(data.password),
        perfil=data.perfil,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user_id: str, data: UserUpdate) -> UserModel:
    user = get_user_by_id(db, user_id)
    if data.nome:
        user.nome = data.nome
    if data.email:
        user.email = data.email
    if data.perfil:
        user.perfil = data.perfil
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: str) -> None:
    user = get_user_by_id(db, user_id)
    db.delete(user)
    db.commit()