from src.modules.payment.data.interfaces.interface_payment_repository import InterfacePaymentRepository
from src.drivers.qrCode.interfaces.qrCode_interface import qrCodeInterface
from src.drivers.notify_api.interfaces.notify_api_interface import NotifyApiInterface
from src.modules.payment.domain.use_cases_interfaces.interface_payment_webhook_use_case import InterPaymentHebhookUseCase
from typing import Dict

class PaymentWebhookUseCase(InterPaymentHebhookUseCase):
    def __init__(self, repository: InterfacePaymentRepository, qr_driver: qrCodeInterface, notify_api: NotifyApiInterface):
        self.__qr_driver = qr_driver
        self.__repository = repository
        self.__notify_api = notify_api
    
    async def process_webhook(self, payment_id: str) -> Dict:

        payment_info = self.__qr_driver.get_payment_info(payment_id)
        
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

         # 2. Notificar a API principal
        notification_success = await self.__notify_api.notify_main_api(schedule_id, new_status)
        
        return {
            "status": new_status,
            "main_api_notified": notification_success
        }