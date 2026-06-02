from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.domain.entities.ticket import TicketStatus


class TicketItemCreate(BaseModel):
    produto_id: str
    quantidade: int = Field(gt=0)
    observacao: Optional[str] = None


class TicketCreate(BaseModel):
    items: list[TicketItemCreate]


class TicketItemResponse(BaseModel):
    id: str
    produto_id: str
    quantidade: int
    observacao: Optional[str] = None
    produto_nome: Optional[str] = None
    produto_preco: Optional[float] = None

    class Config:
        from_attributes = True


class TicketResponse(BaseModel):
    id: str
    comanda_id: str
    status: TicketStatus
    criado_em: datetime
    itens: list[TicketItemResponse] = []

    class Config:
        from_attributes = True


class OrderDetailResponse(BaseModel):
    id: str
    mesa_id: str
    mesa_numero: Optional[int] = None
    status: str
    data_abertura: datetime
    data_fechamento: Optional[datetime] = None
    tickets: list[TicketResponse] = []
    total: float = 0.0

    class Config:
        from_attributes = True


class BillResponse(BaseModel):
    mesa_numero: int
    itens: list[dict]
    total: float
