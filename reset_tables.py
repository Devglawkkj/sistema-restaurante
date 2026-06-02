import sys
sys.path.insert(0, ".")
from app.infrastructure.database.connection import SessionLocal
from app.infrastructure.database.models.table_model import TableModel
from app.domain.entities.table import TableStatus

db = SessionLocal()
tables = db.query(TableModel).all()
for t in tables:
    t.status = TableStatus.livre
db.commit()
print(f"{len(tables)} mesas resetadas para livre!")
db.close()