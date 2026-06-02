# Sistema Restaurante — API

Backend em **FastAPI** para gestão de mesas, comandas, cozinha, pagamentos e relatórios.

Repositório do frontend: [sistema-restaurante-web](https://github.com/Devglawkkj/sistema-restaurante-web)

## Funcionalidades

- Autenticação JWT (admin, garçom, cozinha)
- CRUD de mesas, produtos e usuários
- Comandas com tickets (pedidos à cozinha)
- Pagamentos e fechamento de comanda
- **Liberar mesa** (encerra comanda sem pagamento)
- WebSocket para cozinha e notificações
- Relatórios de vendas e produtos

## Pré-requisitos

- Python 3.11+
- PostgreSQL 16 (recomendado via Docker)
- pip

## Instalação local

```bash
cd restaurant-api
python -m venv .venv
```

**Windows (PowerShell):**

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
docker compose up -d
alembic upgrade head
python create_admin.py
python create_kitchen.py
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Linux / macOS:**

```bash
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
docker compose up -d
alembic upgrade head
python create_admin.py
python create_kitchen.py
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Variáveis de ambiente (`.env`)

| Variável | Descrição |
|----------|-----------|
| `DATABASE_URL` | URL do PostgreSQL |
| `SECRET_KEY` | Chave para assinar tokens JWT |
| `ALGORITHM` | Padrão: `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Expiração do token (padrão: 480) |
| `CORS_ORIGINS` | URLs do frontend separadas por vírgula |

## Documentação da API

Com o servidor rodando:

- Swagger: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Endpoints principais

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/auth/login` | Login |
| GET/POST | `/tables` | Mesas |
| POST | `/tables/{id}/open` | Abrir mesa |
| POST | `/tables/{id}/release` | Liberar mesa |
| GET | `/orders/table/{id}/active` | Comanda ativa da mesa |
| POST | `/orders/{id}/tickets` | Enviar pedido à cozinha |
| POST | `/payments/{order_id}` | Registrar pagamento |
| POST | `/orders/{id}/close` | Fechar comanda |
| GET | `/kitchen/tickets` | Fila da cozinha |
| WS | `/ws/kitchen?token=...` | Atualizações em tempo real |

## Estrutura do projeto

```
restaurant-api/
├── main.py                 # Entrada FastAPI e CORS
├── config.py               # Settings (.env)
├── dependencies.py         # JWT e autorização
├── app/
│   ├── presentation/       # Routers e schemas (API)
│   ├── application/        # Regras de negócio (services)
│   ├── domain/             # Entidades e enums
│   └── infrastructure/     # Banco, modelos, WebSocket
├── migrations/             # Alembic
├── create_admin.py         # Usuário admin inicial
└── create_kitchen.py       # Usuário cozinha inicial
```

## Publicar este repositório (Git)

Este backend é um repositório **independente** do frontend.

```powershell
cd restaurant-api
git status
git add .
git commit -m "feat: descreva sua alteracao"
git push origin main
```

Se for a primeira vez em outra máquina:

```powershell
git clone https://github.com/Devglawkkj/sistema-restaurante.git
cd sistema-restaurante
# siga a instalação acima
```

## Deploy do backend (produção)

O frontend em produção precisa da URL desta API. Exemplo de fluxo:

### Opção A — Render / Railway / Fly.io

1. Crie um PostgreSQL gerenciado (ou use o addon da plataforma).
2. Conecte o repositório `sistema-restaurante`.
3. **Build command:** `pip install -r requirements.txt`
4. **Start command:** `alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Variáveis de ambiente: copie de `.env.example` e ajuste `DATABASE_URL`, `SECRET_KEY`, `CORS_ORIGINS` (URL do site React).

### Opção B — VPS (Linux)

```bash
git clone https://github.com/Devglawkkj/sistema-restaurante.git
cd sistema-restaurante
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # edite com dados reais
alembic upgrade head
# use gunicorn + nginx, ou systemd + uvicorn
```

### CORS em produção

Defina `CORS_ORIGINS` com a URL exata do frontend, por exemplo:

```env
CORS_ORIGINS=https://seu-app.vercel.app
```

## Scripts úteis

| Script | Uso |
|--------|-----|
| `create_admin.py` | Cria/atualiza admin (`admin@restaurante.com` / `admin123`) |
| `create_kitchen.py` | Cria/atualiza cozinha (`cozinha@restaurante.com` / `cozinha123`) |
| `clean_db.py` | Limpa comandas e tickets (desenvolvimento) |

## Licença

Uso educacional / projeto pessoal.
