from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.infrastructure.database.connection import get_db
from app.application.services.auth_service import authenticate_user, create_access_token
from app.presentation.schemas.auth_schema import LoginRequest, TokenResponse

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.email, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha invalidos",
        )
    token = create_access_token({"sub": user.id, "perfil": user.perfil.value})
    return TokenResponse(access_token=token, perfil=user.perfil.value, nome=user.nome)