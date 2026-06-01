from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TicketStatus(str, Enum):
    pendente = "pendente"
    pronto = "pronto"


@dataclass
class Ticket:
    id: str
    comanda_id: str
    status: TicketStatus
    criado_em: datetime
