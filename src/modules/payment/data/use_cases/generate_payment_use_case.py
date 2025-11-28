from src.modules.payment.domain.use_cases_interfaces.interface_generate_payment_use_case import InterfaceGeneratePaymentUseCase
from src.modules.payment.data.interfaces.interface_payment_repository import InterfacePaymentRepository
from src.drivers.qrCode.interfaces.qrCode_interface import qrCodeInterface
from typing import Dict

class GeneratePaymentUseCase(InterfaceGeneratePaymentUseCase):
    def __init__(self, repository: InterfacePaymentRepository, qr_code: qrCodeInterface):
        self.__repository = repository
        self.__qr_code = qr_code
    
    async def payment(self, amount: float, desc: str, email: str, schedule_id: str) -> Dict:

        await self.__payment_exists(schedule_id)

        pix = self.__qr_code.create_payment_pix(
            amount,
            desc,
            email,
            schedule_id
        )

        status = pix["status"]

        await self.save_in_db(status, schedule_id)

        return pix
    
    async def __payment_exists(self, schedule_id: str) -> None:

        payment = await self.__repository.get_payment(schedule_id)

        if payment:
            raise Exception("Pagamento já existe")

    async def save_in_db(self, status: str, schedule_id: str) -> None:

        await self.__repository.generate_payment(status, schedule_id)