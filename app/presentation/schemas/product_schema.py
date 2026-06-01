from pydantic import BaseModel


class ProductCreate(BaseModel):
    nome: str
    preco: float
    categoria: str
    ativo: bool = True


class ProductResponse(BaseModel):
    id: str
    nome: str
    preco: float
    categoria: str
    ativo: bool

    class Config:
        from_attributes = True


class ProductUpdate(BaseModel):
    nome: str | None = None
    preco: float | None = None
    categoria: str | None = None
    ativo: bool | None = None