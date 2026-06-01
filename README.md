# Restaurant API

API do sistema de restaurante construída com FastAPI, SQLAlchemy e PostgreSQL.

## Visão geral

Esta aplicação oferece endpoints para:

- autenticação de usuários
- gerenciamento de mesas
- registro de produtos
- criação de pedidos e tickets
- processamento de pagamentos
- dashboard da cozinha
- relatórios
- notificações via WebSocket

## Pré-requisitos

- Python 3.11+ (ou compatível)
- PostgreSQL 16 (pode ser rodado via Docker Compose)
- pip

## Instalação

No diretório `restaurant-api`, execute:

```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
.venv\Scripts\Activate.ps1 # Windows PowerShell
pip install -r requirements.txt
```

## Configuração de ambiente

Crie um arquivo `.env` na raiz de `restaurant-api` com as variáveis:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/restaurante
SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480
```

A aplicação usa `pydantic-settings` para carregar essas variáveis.

## Banco de dados com Docker Compose

Se quiser usar o banco de dados PostgreSQL via Docker, execute:

```bash
docker-compose up -d
```

O serviço de banco ficará disponível em `localhost:5432`.

## Execução da API

A partir da raiz de `restaurant-api`, rode:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

A API ficará disponível em `http://127.0.0.1:8000`.

## Documentação auto-gerada

Depois de iniciar a API, acesse:

- Swagger UI: `http://127.0.0.1:8000/docs`
- Redoc: `http://127.0.0.1:8000/redoc`

## Criação de usuário administrador

Se houver um script de criação de admin, use-o após configurar o ambiente e o banco:

```bash
python create_admin.py
```

Caso o script não exista ou precise de ajuste, verifique `create_admin.py`.

## Importante

- O frontend `restaurant-web` depende desta API rodando em `http://127.0.0.1:8000`.
- Se o backend estiver em outro host ou porta, atualize `src/services/api.ts` no frontend.

## Estrutura principal

- `main.py` - entrada da aplicação FastAPI
- `config.py` - configuração via variáveis de ambiente
- `dependencies.py` - segurança JWT e autorização
- `app/presentation/routers` - endpoints HTTP
- `app/application/services` - regras de negócio
- `app/infrastructure/database` - conexão e modelos SQLAlchemy
- `app/infrastructure/repositories` - acesso ao banco

---

Este README fornece os passos necessários para instalar, configurar e iniciar o backend do sistema de restaurante.