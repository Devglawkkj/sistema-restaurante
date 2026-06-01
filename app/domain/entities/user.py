from dataclasses import dataclass
from enum import Enum


class UserProfile(str, Enum):
    admin = "admin"
    garcom = "garcom"
    cozinha = "cozinha"


@dataclass
class User:
    id: str
    nome: str
    email: str
    senha_hash: str
    perfil: UserProfile
