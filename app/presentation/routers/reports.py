from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.infrastructure.database.connection import get_db
from app.infrastructure.database.models.order_model import OrderModel
from app.infrastructure.database.models.ticket_model import TicketModel
from app.infrastructure.database.models.ticket_item_model import TicketItemModel
from app.infrastructure.database.models.product_model import ProductModel
from app.infrastructure.database.models.payment_model import PaymentModel
from app.domain.entities.order import OrderStatus
from dependencies import require_admin

router = APIRouter()


@router.get("/sales")
def sales_report(
    date_from: datetime = Query(None),
    date_to: datetime = Query(None),
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    query = db.query(PaymentModel)
    if date_from:
        query = query.filter(PaymentModel.data_pagamento >= date_from)
    if date_to:
        query = query.filter(PaymentModel.data_pagamento <= date_to)

    payments = query.all()
    total = sum(p.valor for p in payments)

    return {
        "total_vendas": total,
        "quantidade_comandas": len(payments),
        "pagamentos": [
            {
                "comanda_id": p.comanda_id,
                "valor": p.valor,
                "metodo": p.metodo,
                "data": p.data_pagamento.isoformat(),
            }
            for p in payments
        ],
    }


@router.get("/products")
def products_report(
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    itens = db.query(TicketItemModel).all()
    contagem = {}

    for item in itens:
        product = db.query(ProductModel).filter(ProductModel.id == item.produto_id).first()
        if not product:
            continue
        if product.id not in contagem:
            contagem[product.id] = {"nome": product.nome, "quantidade": 0, "total": 0.0}
        contagem[product.id]["quantidade"] += item.quantidade
        contagem[product.id]["total"] += product.preco * item.quantidade

    ranking = sorted(contagem.values(), key=lambda x: x["quantidade"], reverse=True)
    return {"produtos_mais_pedidos": ranking}


@router.get("/tables")
def tables_report(
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    orders = db.query(OrderModel).filter(
        OrderModel.status == OrderStatus.fechada,
        OrderModel.data_fechamento.isnot(None),
    ).all()

    result = []
    for order in orders:
        duracao = (order.data_fechamento - order.data_abertura).seconds // 60
        result.append({
            "comanda_id": order.id,
            "mesa_id": order.mesa_id,
            "duracao_minutos": duracao,
            "data_abertura": order.data_abertura.isoformat(),
            "data_fechamento": order.data_fechamento.isoformat(),
        })

    return {"atendimentos": result}