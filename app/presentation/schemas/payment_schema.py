from pydantic import BaseModel, Field
from app.domain.entities.payment import PaymentMethod


class PaymentCreate(BaseModel):
    valor: float = Field(gt=0)
    metodo: PaymentMethod


class PaymentResponse(BaseModel):
    id: str
    comanda_id: str
    valor: float
    metodo: PaymentMethod

    class Config:
        from_attributes = True
