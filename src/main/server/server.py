from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.infra.db.settings.db_metada import init_db
from src.main.routes import generate_payment_routes, webhook_routes, get_payment_routes, health_routes
from src.drivers.messaging.rabbitmq_payment_publisher import RabbitMQPaymentPublisher

# Lifecycle da aplicação
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    
    # Inicializa RabbitMQ (singleton)
    try:
        RabbitMQPaymentPublisher()
    except Exception:
        pass  # Se falhar, vai tentar conectar no primeiro uso
    
    yield
    
    # Shutdown
    try:
        publisher = RabbitMQPaymentPublisher()
        publisher.close()
    except Exception:
        pass

# Inicializa o aplicativo FastAPI
app = FastAPI(
    lifespan=lifespan,
    title="Payments API",
    description="Microserviço de pagamentos via PIX com Mercado Pago",
    version="1.0.0"
)

# Rotas para Endpoints
app.include_router(health_routes.router)
app.include_router(generate_payment_routes.router)
app.include_router(webhook_routes.router)
app.include_router(get_payment_routes.router)