from src.infra.db.repositories.order_repository import OrderRepository
from src.presentation.controllers.generate_payment_controller import GeneratePaymentController
from src.modules.payment.data.use_cases.generate_payment_use_case import GeneratePaymentUseCase
from src.drivers.qrCode.generate_qrCode.qrCode import qrCode
from src.presentation.http_types.http_request import HttpRequest

async def generate_payment_composer(http_request: HttpRequest):

    qr_code = qrCode()

    repository = OrderRepository()

    use_case = GeneratePaymentUseCase(repository, qr_code)

    controller = GeneratePaymentController(use_case)

    return await controller.handle(http_request)
