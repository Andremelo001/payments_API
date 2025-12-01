from src.modules.payment.data.interfaces.interface_payment_repository import InterfacePaymentRepository
from src.drivers.qrCode.interfaces.qrCode_interface import qrCodeInterface
from src.drivers.messaging.interfaces.payment_event_publisher_interface import PaymentEventPublisherInterface
from src.modules.payment.domain.use_cases_interfaces.interface_payment_webhook_use_case import InterfacePaymentHebhookUseCase
from src.errors import MercadoPagoPaymentNotFoundError
from typing import Dict

class PaymentWebhookUseCase(InterfacePaymentHebhookUseCase):
    def __init__(self, repository: InterfacePaymentRepository, qr_driver: qrCodeInterface, event_publisher: PaymentEventPublisherInterface):
        self.__qr_driver = qr_driver
        self.__repository = repository
        self.__event_publisher = event_publisher
    
    async def process_webhook(self, payment_id: str) -> Dict:

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