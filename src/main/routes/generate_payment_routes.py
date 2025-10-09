from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from typing import Dict

from src.presentation.http_types.http_response import HttpResponse

#Import Adapters
from src.main.adapters.request_adapter import request_adapter

#Import Composers
from src.main.composers.generate_payment_composer import generate_payment_composer

router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)

@router.post("/generate_payment", response_model=Dict)
async def generate_payment(request: Request):

    http_response: HttpResponse = await request_adapter(request, generate_payment_composer)

    return JSONResponse(content=http_response.body, status_code=http_response.status_code)