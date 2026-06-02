"""
Servico de comandas (orders): criar/obter comanda por mesa, tickets, total e fechamento.
Resolve comandas duplicadas abertas na mesma mesa (ex.: double-fetch do frontend).
"""
import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.domain.entities.order import OrderStatus
from app.domain.entities.table import TableStatus
from app.domain.entities.ticket import TicketStatus
from app.infrastructure.database.models.order_model import OrderModel
from app.infrastructure.database.models.product_model import ProductModel
from app.infrastructure.database.models.table_model import TableModel
from app.infrastructure.database.models.ticket_item_model import TicketItemModel
from app.infrastructure.database.models.ticket_model import TicketModel
from app.presentation.schemas.ticket_schema import TicketCreate


def _get_order(db: Session, order_id: str) -> OrderModel:
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comanda nao encontrada")
    return order


def calculate_order_total(db: Session, order_id: str) -> float:
    tickets = (
        db.query(TicketModel)
        .options(joinedload(TicketModel.itens).joinedload(TicketItemModel.produto))
        .filter(TicketModel.comanda_id == order_id)
        .all()
    )
    total = 0.0
    for ticket in tickets:
        for item in ticket.itens:
            if item.produto:
                total += item.produto.preco * item.quantidade
    return total


def _build_order_detail(db: Session, order: OrderModel) -> dict:
    table = db.query(TableModel).filter(TableModel.id == order.mesa_id).first()
    tickets = (
        db.query(TicketModel)
        .options(joinedload(TicketModel.itens).joinedload(TicketItemModel.produto))
        .filter(TicketModel.comanda_id == order.id)
        .order_by(TicketModel.criado_em)
        .all()
    )

    tickets_data = []
    for ticket in tickets:
        itens_data = []
        for item in ticket.itens:
            product = item.produto
            itens_data.append({
                "id": item.id,
                "produto_id": item.produto_id,
                "quantidade": item.quantidade,
                "observacao": item.observacao,
                "produto_nome": product.nome if product else "Desconhecido",
                "produto_preco": product.preco if product else 0.0,
            })
        tickets_data.append({
            "id": ticket.id,
            "comanda_id": ticket.comanda_id,
            "status": ticket.status.value if isinstance(ticket.status, TicketStatus) else ticket.status,
            "criado_em": ticket.criado_em,
            "itens": itens_data,
        })

    return {
        "id": order.id,
        "mesa_id": order.mesa_id,
        "mesa_numero": table.numero if table else None,
        "status": order.status.value,
        "data_abertura": order.data_abertura,
        "data_fechamento": order.data_fechamento,
        "tickets": tickets_data,
        "total": round(calculate_order_total(db, order.id), 2),
    }


def get_order_detail(db: Session, order_id: str) -> dict:
    return _build_order_detail(db, _get_order(db, order_id))


def _ticket_count(db: Session, order_id: str) -> int:
    return db.query(TicketModel).filter(TicketModel.comanda_id == order_id).count()


def _resolve_open_orders(db: Session, orders: list[OrderModel]) -> OrderModel:
    """Escolhe a comanda correta quando existem duplicatas abertas na mesma mesa."""
    if len(orders) == 1:
        return orders[0]

    from app.infrastructure.database.models.payment_model import PaymentModel

    def _order_priority(o: OrderModel) -> tuple:
        opened_ts = o.data_abertura.timestamp() if o.data_abertura else 0
        return (_ticket_count(db, o.id), opened_ts)

    primary = max(orders, key=_order_priority)

    for order in orders:
        if order.id == primary.id:
            continue
        if _ticket_count(db, order.id) > 0:
            continue
        has_payment = db.query(PaymentModel).filter(PaymentModel.comanda_id == order.id).first()
        if not has_payment:
            db.delete(order)

    db.commit()
    db.refresh(primary)
    return primary


def get_active_order_for_table(db: Session, table_id: str) -> OrderModel | None:
    table = db.query(TableModel).filter(TableModel.id == table_id).first()
    if not table:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mesa nao encontrada")

    open_orders = (
        db.query(OrderModel)
        .filter(OrderModel.mesa_id == table_id, OrderModel.status == OrderStatus.aberta)
        .order_by(OrderModel.data_abertura.desc())
        .all()
    )
    if not open_orders:
        return None
    return _resolve_open_orders(db, open_orders)


def get_or_create_order(db: Session, table_id: str) -> OrderModel:
    table = db.query(TableModel).filter(TableModel.id == table_id).first()
    if not table:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mesa nao encontrada")

    existing = get_active_order_for_table(db, table_id)
    if existing:
        return existing

    order = OrderModel(
        id=str(uuid.uuid4()),
        mesa_id=table_id,
        status=OrderStatus.aberta,
    )
    db.add(order)
    if table.status == TableStatus.livre:
        table.status = TableStatus.ocupada
    db.commit()
    db.refresh(order)
    return order


def add_ticket(db: Session, order_id: str, data: TicketCreate) -> TicketModel:
    order = _get_order(db, order_id)
    if order.status != OrderStatus.aberta:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Comanda ja foi fechada",
        )
    if not data.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O pedido deve conter ao menos um item",
        )

    ticket_id = str(uuid.uuid4())
    ticket = TicketModel(
        id=ticket_id,
        comanda_id=order_id,
        status=TicketStatus.pendente,
    )
    db.add(ticket)

    for item_data in data.items:
        if item_data.quantidade <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantidade deve ser maior que zero",
            )
        product = db.query(ProductModel).filter(ProductModel.id == item_data.produto_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Produto {item_data.produto_id} nao encontrado",
            )
        if not product.ativo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Produto '{product.nome}' esta inativo",
            )
        db.add(
            TicketItemModel(
                id=str(uuid.uuid4()),
                ticket_id=ticket_id,
                produto_id=item_data.produto_id,
                quantidade=item_data.quantidade,
                observacao=item_data.observacao,
            )
        )

    db.commit()
    db.refresh(ticket)
    return ticket


def get_order_bill(db: Session, order_id: str) -> dict:
    detail = get_order_detail(db, order_id)
    itens = []
    for ticket in detail["tickets"]:
        for item in ticket["itens"]:
            itens.append({
                "produto_nome": item["produto_nome"],
                "quantidade": item["quantidade"],
                "preco_unitario": item["produto_preco"],
                "subtotal": item["produto_preco"] * item["quantidade"],
            })
    return {
        "mesa_numero": detail["mesa_numero"],
        "itens": itens,
        "total": detail["total"],
    }


def close_order(db: Session, order_id: str) -> OrderModel:
    from app.infrastructure.database.models.payment_model import PaymentModel

    order = _get_order(db, order_id)
    if order.status != OrderStatus.aberta:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Comanda ja esta fechada",
        )

    payment = db.query(PaymentModel).filter(PaymentModel.comanda_id == order_id).first()
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registre o pagamento antes de fechar a comanda",
        )

    order.status = OrderStatus.fechada
    order.data_fechamento = datetime.now(timezone.utc)

    table = db.query(TableModel).filter(TableModel.id == order.mesa_id).first()
    if table:
        table.status = TableStatus.livre

    db.commit()
    db.refresh(order)
    return order
