import sys
sys.path.insert(0, ".")
from app.infrastructure.database.connection import SessionLocal
from app.infrastructure.database.models.order_model import OrderModel
from app.infrastructure.database.models.ticket_model import TicketModel
from app.infrastructure.database.models.ticket_item_model import TicketItemModel
from app.infrastructure.database.models.payment_model import PaymentModel
from app.infrastructure.database.models.table_model import TableModel
from app.domain.entities.table import TableStatus

db = SessionLocal()

db.query(TicketItemModel).delete()
db.query(TicketModel).delete()
db.query(PaymentModel).delete()
db.query(OrderModel).delete()

tables = db.query(TableModel).all()
for t in tables:
    t.status = TableStatus.livre

db.commit()
print("Banco limpo! Mesas, comandas e tickets resetados.")
db.close()