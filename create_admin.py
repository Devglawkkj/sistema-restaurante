import sys

sys.path.insert(0, ".")
from app.infrastructure.database.connection import SessionLocal
from app.infrastructure.database.models.user_model import UserModel
from app.application.services.auth_service import hash_password
from app.domain.entities.user import UserProfile
import uuid

ADMIN_EMAIL = "admin@restaurante.com"
ADMIN_PASSWORD = "admin123"

db = SessionLocal()
admin = db.query(UserModel).filter(UserModel.email == ADMIN_EMAIL).first()

if admin:
    admin.senha_hash = hash_password(ADMIN_PASSWORD)
    admin.perfil = UserProfile.admin
    admin.nome = "Administrador"
    db.commit()
    print(f"Senha do admin atualizada: {ADMIN_EMAIL} / {ADMIN_PASSWORD}")
else:
    admin = UserModel(
        id=str(uuid.uuid4()),
        nome="Administrador",
        email=ADMIN_EMAIL,
        senha_hash=hash_password(ADMIN_PASSWORD),
        perfil=UserProfile.admin,
    )
    db.add(admin)
    db.commit()
    print(f"Admin criado: {ADMIN_EMAIL} / {ADMIN_PASSWORD}")

db.close()
