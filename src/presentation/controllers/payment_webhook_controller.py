from src.modules.payment.domain.use_cases_interfaces.interface_payment_webhook_use_case import InterPaymentHebhookUseCase
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class PaymentWebhookController(ControllerInterface):
    def __init__(self, use_case: InterPaymentHebhookUseCase):
        self.__use_case = use_case
    
    async def handle(self, http_request: HttpRequest) -> HttpResponse:

        payment_id = http_request.body["data"]["id"]

        response = await self.__use_case.process_webhook(payment_id)

        return HttpResponse(
            status_code=200,
            body = {
                "data": response
            }
        )