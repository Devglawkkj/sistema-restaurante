from datetime import datetime
from pydantic import BaseModel
from app.domain.entities.order import OrderStatus


class OrderResponse(BaseModel):
    id: str
    mesa_id: str
    status: OrderStatus
    data_abertura: datetime
    data_fechamento: datetime | None = None

    class Config:
        from_attributes = True
