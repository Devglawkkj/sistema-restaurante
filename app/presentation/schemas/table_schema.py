# Schemas Pydantic para validacao e serializacao de dados de mesa.
# Esses modelos definem como as entradas sao recebidas e como as respostas sao retornadas ao cliente.
from pydantic import BaseModel
from app.domain.entities.table import TableStatus


class TableCreate(BaseModel):
    numero: int


class TableResponse(BaseModel):
    id: str
    numero: int
    status: TableStatus

    class Config:
        from_attributes = True


class TableUpdate(BaseModel):
    numero: int | None = None