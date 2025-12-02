from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from typing import Dict

from src.presentation.http_types.http_response import HttpResponse

#Import Adapters
from src.main.adapters.request_adapter import request_adapter

#Import Composers
from src.main.composers.payment_webhook_composer import payment_webhook_composer

router = APIRouter(
    prefix="/webhook",
    tags=["Webhooks"],
)

@router.post("/mercadopago", response_model=Dict)
async def mercado_pago_webhook(request: Request):
    
    http_response: HttpResponse = await request_adapter(request, payment_webhook_composer)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)