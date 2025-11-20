from src.infra.db.repositories.order_repository import OrderRepository
from src.presentation.controllers.get_payment_controller import GetPaymentController
from src.modules.payment.data.use_cases.get_payment_use_case import GetPaymentUseCase
from src.presentation.http_types.http_request import HttpRequest

async def get_payment_composer(http_request: HttpRequest):

    repository = OrderRepository()

    use_case = GetPaymentUseCase(repository)

    controller = GetPaymentController(use_case)

    return await controller.handle(http_request)
