from src.errors.types_errors import (
    PaymentAlreadyExistsError,
    PaymentNotFoundError,
    MercadoPagoError,
    MercadoPagoPaymentNotFoundError,
    NotificationError,
    ValidationError,
    QrCodeGenerationError,
    WebhookValidationError
)
from src.presentation.http_types.http_response import HttpResponse

def handle_errors(error: Exception) -> HttpResponse:
    """
    Centraliza o tratamento de erros da aplicação.
    Mapeia exceções customizadas para respostas HTTP apropriadas.
    """
    
    # Erros de domínio de pagamento
    if isinstance(error, PaymentAlreadyExistsError):
        return HttpResponse(
            status_code=error.status_code,
            body={
                "errors": [{
                    "title": error.name,
                    "detail": error.message,
                    "schedule_id": error.schedule_id
                }]
            }
        )
    
    if isinstance(error, PaymentNotFoundError):
        return HttpResponse(
            status_code=error.status_code,
            body={
                "errors": [{
                    "title": error.name,
                    "detail": error.message,
                    "identifier": error.identifier,
                    "identifier_type": error.identifier_type
                }]
            }
        )
    
    # Erros do Mercado Pago
    if isinstance(error, MercadoPagoPaymentNotFoundError):
        return HttpResponse(
            status_code=error.status_code,
            body={
                "errors": [{
                    "title": error.name,
                    "detail": error.message,
                    "payment_id": error.payment_id
                }]
            }
        )
    
    if isinstance(error, MercadoPagoError):
        return HttpResponse(
            status_code=error.status_code,
            body={
                "errors": [{
                    "title": error.name,
                    "detail": error.message
                }]
            }
        )
    
    # Erros de validação
    if isinstance(error, ValidationError):
        return HttpResponse(
            status_code=error.status_code,
            body={
                "errors": [{
                    "title": error.name,
                    "detail": error.message,
                    "field": error.field
                }]
            }
        )
    
    # Erros de webhook
    if isinstance(error, WebhookValidationError):
        return HttpResponse(
            status_code=error.status_code,
            body={
                "errors": [{
                    "title": error.name,
                    "detail": error.message
                }]
            }
        )
    
    # Erros de QR Code
    if isinstance(error, QrCodeGenerationError):
        return HttpResponse(
            status_code=error.status_code,
            body={
                "errors": [{
                    "title": error.name,
                    "detail": error.message,
                    "schedule_id": error.schedule_id
                }]
            }
        )
    
    # Erros de notificação (não devem ser retornados ao cliente, mas logados)
    if isinstance(error, NotificationError):
        return HttpResponse(
            status_code=error.status_code,
            body={
                "errors": [{
                    "title": error.name,
                    "detail": "Failed to notify external service. Payment status updated locally.",
                    "schedule_id": error.schedule_id
                }]
            }
        )
    
    # Erro genérico não tratado
    return HttpResponse(
        status_code=500,
        body={
            "errors": [{
                "title": "InternalServerError",
                "detail": "An unexpected error occurred. Please try again later."
            }]
        }
    )
