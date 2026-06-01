import uuid
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.infrastructure.database.models.product_model import ProductModel
from app.presentation.schemas.product_schema import ProductCreate, ProductUpdate


def get_all_products(db: Session, apenas_ativos: bool = False):
    query = db.query(ProductModel)
    if apenas_ativos:
        query = query.filter(ProductModel.ativo == True)
    return query.all()


def get_product_by_id(db: Session, product_id: str) -> ProductModel:
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado")
    return product


def create_product(db: Session, data: ProductCreate) -> ProductModel:
    product = ProductModel(
        id=str(uuid.uuid4()),
        nome=data.nome,
        preco=data.preco,
        categoria=data.categoria,
        ativo=data.ativo,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(db: Session, product_id: str, data: ProductUpdate) -> ProductModel:
    product = get_product_by_id(db, product_id)
    if data.nome is not None:
        product.nome = data.nome
    if data.preco is not None:
        product.preco = data.preco
    if data.categoria is not None:
        product.categoria = data.categoria
    if data.ativo is not None:
        product.ativo = data.ativo
    db.commit()
    db.refresh(product)
    return product


def toggle_product(db: Session, product_id: str) -> ProductModel:
    product = get_product_by_id(db, product_id)
    product.ativo = not product.ativo
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: str) -> None:
    product = get_product_by_id(db, product_id)
    db.delete(product)
    db.commit()