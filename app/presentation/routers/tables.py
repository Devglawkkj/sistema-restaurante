# Roteador de mesas. Define os endpoints HTTP para listar, criar, atualizar,
# abrir, fechar e excluir mesas. As autorizacoes sao aplicadas via dependencias.
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infrastructure.database.connection import get_db
from app.application.services import table_service
from app.presentation.schemas.table_schema import TableCreate, TableUpdate, TableResponse
from dependencies import get_current_user, require_admin

router = APIRouter()


@router.get("", response_model=list[TableResponse])
def list_tables(
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    return table_service.get_all_tables(db)


@router.post("", response_model=TableResponse, status_code=201)
def create_table(
    data: TableCreate,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    # Cria uma nova mesa apenas se o usuario for administrador.
    return table_service.create_table(db, data)


@router.get("/{table_id}", response_model=TableResponse)
def get_table(
    table_id: str,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    return table_service.get_table_by_id(db, table_id)


@router.put("/{table_id}", response_model=TableResponse)
def update_table(
    table_id: str,
    data: TableUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    return table_service.update_table(db, table_id, data)


@router.post("/{table_id}/open", response_model=TableResponse)
def open_table(
    table_id: str,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    return table_service.open_table(db, table_id)


@router.post("/{table_id}/close", response_model=TableResponse)
def close_table(
    table_id: str,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    return table_service.close_table(db, table_id)


@router.post("/{table_id}/release", response_model=TableResponse)
def release_table(
    table_id: str,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    return table_service.release_table(db, table_id)


@router.delete("/{table_id}", status_code=204)
def delete_table(
    table_id: str,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    table_service.delete_table(db, table_id)