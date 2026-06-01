from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class OrderStatus(str, Enum):
    aberta = "aberta"
    fechada = "fechada"


@dataclass
class Order:
    id: str
    mesa_id: str
    status: OrderStatus
    data_abertura: datetime
    data_fechamento: Optional[datetime] = None
