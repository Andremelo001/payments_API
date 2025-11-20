from src.modules.payment.domain.use_cases_interfaces.interface_get_payment_use_case import InterfaceGetPaymentUseCase
from src.modules.payment.data.interfaces.interface_payment_repository import InterfacePaymentRepository
from src.modules.payment.domain.models.order import OrderModel
from typing import Dict

class GetPaymentUseCase(InterfaceGetPaymentUseCase):
    def __init__(self, repository: InterfacePaymentRepository):
        self.__repository = repository
    
    async def get_payment(self, schedule_id: str) -> Dict:

        payment = await self.__repository.get_payment(schedule_id)

        return self.__format_response(payment)

    def __format_response(self, payment: OrderModel) -> Dict:

        return {
            "id": str(payment.id),
            "id_schedule": payment.id_schedule,
            "status_payment": payment.status_payment,
            "date_payment": str(payment.date_payment)
        }