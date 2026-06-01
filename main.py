# Aplicacao principal do backend. Define a instancia FastAPI, habilita CORS e registra os roteadores.
# Cada router e responsavel por expor os endpoints de um modulo do restaurante.
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.presentation.routers import (
    auth,
    users,
    tables,
    products,
    orders,
    payments,
    kitchen,
    reports,
    websocket,
)

app = FastAPI(
    title="Sistema de Restaurante",
    version="1.0.0",
    description="API para gerenciamento de pedidos de restaurante",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,      prefix="/auth",     tags=["Autenticacao"])
app.include_router(users.router,     prefix="/users",    tags=["Usuarios"])
app.include_router(tables.router,    prefix="/tables",   tags=["Mesas"])
app.include_router(products.router,  prefix="/products", tags=["Produtos"])
app.include_router(orders.router,    prefix="/orders",   tags=["Comandas"])
app.include_router(payments.router,  prefix="/payments", tags=["Pagamentos"])
app.include_router(kitchen.router,   prefix="/kitchen",  tags=["Cozinha"])
app.include_router(reports.router,   prefix="/reports",  tags=["Relatorios"])
app.include_router(websocket.router, tags=["WebSocket"])


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "Sistema de Restaurante rodando"}
