from dataclasses import dataclass
from typing import Optional


@dataclass
class Product:
    id: str
    nome: str
    preco: float
    categoria: str
    ativo: bool = True
