from fastapi import APIRouter, HTTPException
from src.infra.db.settings.db_connection_handler import db_connection_handler
from sqlalchemy import text
import httpx

router = APIRouter(tags=["Health"])

@router.get("/health")
async def health():
    """
    Liveness probe - verifica se o processo está vivo.
    Usado por Docker/Kubernetes para saber se deve reiniciar o container.
    """
    return {
        "status": "healthy",
        "service": "payments-api",
        "version": "1.0.0"
    }

@router.get("/ready")
async def readiness():
    """
    Readiness probe - verifica se o serviço está pronto para processar requisições.
    Testa conexão com banco de dados e disponibilidade do Mercado Pago.
    Usado por load balancers para saber se deve enviar tráfego.
    """
    checks = {
        "database": False,
        "mercadopago": False
    }
    errors = []
    
    # Testa conexão com banco de dados
    try:
        async for session in db_connection_handler.get_session():
            await session.execute(text("SELECT 1"))
            checks["database"] = True
            break
    except Exception as e:
        errors.append(f"Database error: {str(e)}")
    
    # Testa disponibilidade da API do Mercado Pago
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            response = await client.get("https://api.mercadopago.com")
            # Considera OK se não for erro 5xx (servidor indisponível)
            if response.status_code < 500:
                checks["mercadopago"] = True
    except Exception as e:
        errors.append(f"Mercado Pago error: {str(e)}")
    
    # Se algum check falhou, retorna 503 (Service Unavailable)
    if not all(checks.values()):
        raise HTTPException(
            status_code=503,
            detail={
                "status": "not ready",
                "checks": checks,
                "errors": errors
            }
        )
    
    return {
        "status": "ready",
        "checks": checks
    }
