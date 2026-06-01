from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.infrastructure.database.connection import get_db
from app.application.services import product_service
from app.presentation.schemas.product_schema import ProductCreate, ProductUpdate, ProductResponse
from dependencies import get_current_user, require_admin

router = APIRouter()


@router.get("", response_model=list[ProductResponse])
def list_products(
    apenas_ativos: bool = Query(False),
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    return product_service.get_all_products(db, apenas_ativos)


@router.post("", response_model=ProductResponse, status_code=201)
def create_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    return product_service.create_product(db, data)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: str,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    return product_service.get_product_by_id(db, product_id)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: str,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    return product_service.update_product(db, product_id, data)


@router.patch("/{product_id}/toggle", response_model=ProductResponse)
def toggle_product(
    product_id: str,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    return product_service.toggle_product(db, product_id)


@router.delete("/{product_id}", status_code=204)
def delete_product(
    product_id: str,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    product_service.delete_product(db, product_id)