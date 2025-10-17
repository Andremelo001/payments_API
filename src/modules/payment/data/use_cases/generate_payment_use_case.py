from src.modules.payment.domain.use_cases_interfaces.interface_generate_payment_use_case import InterfaceGeneratePaymentUseCase
from src.modules.payment.data.interfaces.interface_payment_repository import InterfacePaymentRepository
from src.drivers.qrCode.generate_qrCode.qrCode import qr_code
from typing import Dict

class GeneratePaymentUseCase(InterfaceGeneratePaymentUseCase):
    def __init__(self, repository: InterfacePaymentRepository):
        self.__repository = repository
    
    async def payment(self, amount: float, desc: str, email: str) -> Dict:

        pix = qr_code.create_payment_pix(
            amount,
            desc,
            email,
        )

        status = pix["status"]

        await self.save_in_db(status)

        return pix

    async def save_in_db(self, status: str) -> None:

        await self.__repository.generate_payment(status)