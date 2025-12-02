from src.modules.payment.data.interfaces.interface_payment_repository import InterfacePaymentRepository
from src.drivers.qrCode.interfaces.qrCode_interface import qrCodeInterface
from src.drivers.messaging.interfaces.payment_event_publisher_interface import PaymentEventPublisherInterface
from src.modules.payment.domain.use_cases_interfaces.interface_payment_webhook_use_case import InterfacePaymentHebhookUseCase
from src.errors import MercadoPagoPaymentNotFoundError, WebhookValidationError
from typing import Dict
import hmac
import hashlib
import os

class PaymentWebhookUseCase(InterfacePaymentHebhookUseCase):
    def __init__(self, repository: InterfacePaymentRepository, qr_driver: qrCodeInterface, event_publisher: PaymentEventPublisherInterface):
        self.__qr_driver = qr_driver
        self.__repository = repository
        self.__event_publisher = event_publisher
        self.__secret_webhook = os.getenv("MERCADOPAGO_WEBHOOK_SECRET")
    
    async def process_webhook(self, payment_id: str, x_signature: str = "", x_request_id: str = "") -> Dict:

        # Valida assinatura
        if not self.__validate_signature(x_signature, x_request_id, payment_id):
            raise WebhookValidationError("Invalid webhook signature")

        payment_info = await self.__qr_driver.get_payment_info(payment_id)

        if not payment_info:
            raise MercadoPagoPaymentNotFoundError(payment_id)
        
        status = payment_info.get("status")
        
        schedule_id = payment_info.get("external_reference")

        # Mapear status do Mercado Pago para seu sistema
        status_mapping = {
            "approved": "paid",
            "pending": "pending", 
            "in_process": "pending",
            "rejected": "rejected",
            "cancelled": "rejected"
        }

        new_status = status_mapping.get(status, "pending")
        
        # 1. Atualizar no banco local do microserviço
        await self.__repository.update_status_payment(new_status=new_status, schedule_id=schedule_id)

        event = {
            "event": "payment_updated",
            "schedule_id": schedule_id,
            "payment_id": payment_info.get("id"),
            "status": new_status,
        }

        await self.__event_publisher.publish_payment_event(event)
        
        return {
            "status": new_status,
            "event_published": True
        }
    
    def __validate_signature(self, x_signature: str, x_request_id: str, data_id: str) -> bool:
        """Valida assinatura do webhook Mercado Pago."""
        # Modo dev: se não configurado, aceita
        if not self.__secret_webhook:
            return True
        
        try:
            # Extrai ts e hash do header x-signature
            parts = dict(part.split("=") for part in x_signature.split(",") if "=" in part)
            ts = parts.get("ts")
            received_hash = parts.get("v1")
            
            if not ts or not received_hash:
                return False
            
            # Monta manifest e calcula HMAC
            manifest = f"id:{data_id};request-id:{x_request_id};ts:{ts};"
            calculated_hash = hmac.new(
                self.__secret_webhook.encode(),
                manifest.encode(),
                hashlib.sha256
            ).hexdigest()
            
            return hmac.compare_digest(calculated_hash, received_hash)
            
        except Exception:
            return False