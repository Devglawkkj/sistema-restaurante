from pydantic import BaseModel, EmailStr
from app.domain.entities.user import UserProfile


class UserCreate(BaseModel):
    nome: str
    email: EmailStr
    password: str
    perfil: UserProfile


class UserResponse(BaseModel):
    id: str
    nome: str
    email: str
    perfil: UserProfile

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    nome: str | None = None
    email: EmailStr | None = None
    perfil: UserProfile | None = None