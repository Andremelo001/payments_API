from src.modules.payment.domain.use_cases_interfaces.interface_generate_payment_use_case import InterfaceGeneratePaymentUseCase
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

class GeneratePaymentController(ControllerInterface):
    def __init__(self, use_case: InterfaceGeneratePaymentUseCase):
        self.__use_case = use_case
    
    async def handle(self, http_request: HttpRequest) -> HttpResponse:

        amount = http_request.body["amount"]
        desc = http_request.body["desc"]
        email = http_request.body["email"]

        response = await self.__use_case.payment(amount, desc, email)

        return HttpResponse(
            status_code=200,
            body = {
                "data": response
            }
        )
