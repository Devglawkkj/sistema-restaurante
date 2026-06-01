from dataclasses import dataclass
from enum import Enum


class TableStatus(str, Enum):
    livre = "livre"
    ocupada = "ocupada"


@dataclass
class Table:
    id: str
    numero: int
    status: TableStatus
