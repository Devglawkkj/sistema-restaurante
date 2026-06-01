from dataclasses import dataclass
from typing import Optional


@dataclass
class TicketItem:
    id: str
    ticket_id: str
    produto_id: str
    quantidade: int
    observacao: Optional[str] = None
