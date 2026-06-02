# Dependencias de seguranca utilizadas nos endpoints. Essas funcoes cuidam da verificacao de tokens JWT
# e da autorizacao de acesso baseado no perfil do usuario.
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.infrastructure.database.connection import get_db
from config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def verify_token_optional(token: str) -> dict | None:
    try:
        return decode_access_token(token)
    except HTTPException:
        return None


def decode_access_token(token: str) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return {"user_id": str(user_id), "perfil": payload.get("perfil")}
    except JWTError:
        raise credentials_exception


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    return decode_access_token(token)


def require_admin(current_user: dict = Depends(get_current_user)):
    if current_user["perfil"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a administradores",
        )
    return current_user
