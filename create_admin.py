import sys
sys.path.insert(0, ".")
from app.infrastructure.database.connection import SessionLocal
from app.infrastructure.database.models.user_model import UserModel
from app.application.services.auth_service import hash_password
from app.domain.entities.user import UserProfile
import uuid

db = SessionLocal()
admin = UserModel(
    id=str(uuid.uuid4()),
    nome="Administrador",
    email="admin@restaurante.com",
    senha_hash=hash_password("admin123"),
    perfil=UserProfile.admin,
)
db.add(admin)
db.commit()
print("Admin criado com sucesso!")
db.close()