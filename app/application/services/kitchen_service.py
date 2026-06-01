from sqlalchemy.orm import Session
from app.infrastructure.database.models.ticket_model import TicketModel
from app.infrastructure.database.models.ticket_item_model import TicketItemModel
from app.infrastructure.database.models.product_model import ProductModel
from app.infrastructure.database.models.order_model import OrderModel
from app.infrastructure.database.models.table_model import TableModel
from app.domain.entities.ticket import TicketStatus


def get_pending_tickets(db: Session) -> list:
    tickets = db.query(TicketModel).filter(
        TicketModel.status == TicketStatus.pendente
    ).order_by(TicketModel.criado_em).all()

    result = []
    for ticket in tickets:
        order = db.query(OrderModel).filter(OrderModel.id == ticket.comanda_id).first()
        table = db.query(TableModel).filter(TableModel.id == order.mesa_id).first() if order else None
        itens = db.query(TicketItemModel).filter(TicketItemModel.ticket_id == ticket.id).all()

        itens_data = []
        for item in itens:
            product = db.query(ProductModel).filter(ProductModel.id == item.produto_id).first()
            itens_data.append({
                "produto_nome": product.nome if product else "Desconhecido",
                "quantidade": item.quantidade,
                "observacao": item.observacao,
            })

        result.append({
            "ticket_id": ticket.id,
            "mesa_numero": table.numero if table else 0,
            "criado_em": ticket.criado_em.isoformat(),
            "itens": itens_data,
        })

    return result