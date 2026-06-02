# Servico de dominio para operacoes de mesa. Este modulo orquestra validacoes e
# persistencia via SQLAlchemy, mantendo as regras de negocio separadas dos endpoints.
import uuid
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.infrastructure.database.models.table_model import TableModel
from app.domain.entities.table import TableStatus
from app.presentation.schemas.table_schema import TableCreate, TableUpdate


def get_all_tables(db: Session):
    return db.query(TableModel).order_by(TableModel.numero).all()


def get_table_by_id(db: Session, table_id: str) -> TableModel:
    table = db.query(TableModel).filter(TableModel.id == table_id).first()
    if not table:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mesa nao encontrada")
    return table


def create_table(db: Session, data: TableCreate) -> TableModel:
    # Verifica se o numero de mesa ja esta cadastrado antes de inserir.
    existing = db.query(TableModel).filter(TableModel.numero == data.numero).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Numero de mesa ja existe")
    table = TableModel(
        id=str(uuid.uuid4()),
        numero=data.numero,
        status=TableStatus.livre,
    )
    db.add(table)
    db.commit()
    db.refresh(table)
    return table


def update_table(db: Session, table_id: str, data: TableUpdate) -> TableModel:
    table = get_table_by_id(db, table_id)
    if data.numero is not None:
        table.numero = data.numero
    db.commit()
    db.refresh(table)
    return table


def open_table(db: Session, table_id: str) -> TableModel:
    table = get_table_by_id(db, table_id)
    if table.status == TableStatus.ocupada:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Mesa ja esta ocupada")
    table.status = TableStatus.ocupada
    db.commit()
    db.refresh(table)
    return table


def close_table(db: Session, table_id: str) -> TableModel:
    from app.infrastructure.database.models.order_model import OrderModel
    from app.domain.entities.order import OrderStatus

    table = get_table_by_id(db, table_id)

    comanda_aberta = db.query(OrderModel).filter(
        OrderModel.mesa_id == table_id,
        OrderModel.status == OrderStatus.aberta,
    ).first()

    if comanda_aberta:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Mesa possui comanda aberta. Realize o pagamento ou libere a mesa.",
        )

    table.status = TableStatus.livre
    db.commit()
    db.refresh(table)
    return table


def release_table(db: Session, table_id: str) -> TableModel:
    """
    Libera a mesa para novo atendimento.
    Fecha todas as comandas abertas sem registrar pagamento (cancelamento/desistencia).
    Diferente de close_table, que exige que nao haja comanda aberta.
    """
    from datetime import datetime, timezone

    from app.infrastructure.database.models.order_model import OrderModel
    from app.domain.entities.order import OrderStatus

    table = get_table_by_id(db, table_id)

    open_orders = (
        db.query(OrderModel)
        .filter(OrderModel.mesa_id == table_id, OrderModel.status == OrderStatus.aberta)
        .all()
    )

    now = datetime.now(timezone.utc)
    for order in open_orders:
        order.status = OrderStatus.fechada
        order.data_fechamento = now

    table.status = TableStatus.livre
    db.commit()
    db.refresh(table)
    return table


def delete_table(db: Session, table_id: str) -> None:
    from app.infrastructure.database.models.order_model import OrderModel

    table = get_table_by_id(db, table_id)
    has_orders = db.query(OrderModel).filter(OrderModel.mesa_id == table_id).first()
    if has_orders:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Mesa possui comandas vinculadas e nao pode ser excluida",
        )
    db.delete(table)
    db.commit()