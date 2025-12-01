from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.infra.db.settings.db_metada import init_db
from src.main.routes import generate_payment_routes, webhook_routes, get_payment_routes

# Configurações de inicialização do banco 
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

# Inicializa o aplicativo FastAPI
app = FastAPI(
    lifespan=lifespan,
    title="Payments API",
    description="Microserviço de pagamentos via PIX com Mercado Pago",
    version="1.0.0"
)

# Rotas para Endpoints
app.include_router(generate_payment_routes.router)
app.include_router(webhook_routes.router)
app.include_router(get_payment_routes.router)