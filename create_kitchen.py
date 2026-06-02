import sys

sys.path.insert(0, ".")
from app.infrastructure.database.connection import SessionLocal
from app.infrastructure.database.models.user_model import UserModel
from app.application.services.auth_service import hash_password
from app.domain.entities.user import UserProfile
import uuid

KITCHEN_EMAIL = "cozinha@restaurante.com"
KITCHEN_PASSWORD = "cozinha123"

db = SessionLocal()
user = db.query(UserModel).filter(UserModel.email == KITCHEN_EMAIL).first()

if user:
    user.senha_hash = hash_password(KITCHEN_PASSWORD)
    user.perfil = UserProfile.cozinha
    user.nome = "Cozinha"
    db.commit()
    print(f"Senha da cozinha atualizada: {KITCHEN_EMAIL} / {KITCHEN_PASSWORD}")
else:
    user = UserModel(
        id=str(uuid.uuid4()),
        nome="Cozinha",
        email=KITCHEN_EMAIL,
        senha_hash=hash_password(KITCHEN_PASSWORD),
        perfil=UserProfile.cozinha,
    )
    db.add(user)
    db.commit()
    print(f"Usuario de cozinha criado: {KITCHEN_EMAIL} / {KITCHEN_PASSWORD}")

db.close()
