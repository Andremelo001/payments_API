from src.infra.db.repositories.order_repository import OrderRepository
from src.presentation.controllers.payment_webhook_controller import PaymentWebhookController
from src.modules.payment.data.use_cases.payment_webhook_use_case import PaymentWebhookUseCase
from src.drivers.qrCode.generate_qrCode.qrCode import qrCode
from src.drivers.notify_api.notify_apy import NotifyApi
from src.presentation.http_types.http_request import HttpRequest

async def payment_webhook_composer(http_request: HttpRequest):

    qr_code = qrCode()

    notify_api = NotifyApi()

    repository = OrderRepository()

    use_case = PaymentWebhookUseCase(repository, qr_code, notify_api)

    controller = PaymentWebhookController(use_case)

    return await controller.handle(http_request)
