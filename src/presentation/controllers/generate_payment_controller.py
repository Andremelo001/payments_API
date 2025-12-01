from src.modules.payment.domain.use_cases_interfaces.interface_generate_payment_use_case import InterfaceGeneratePaymentUseCase
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.errors import handle_errors, ValidationError

class GeneratePaymentController(ControllerInterface):
    def __init__(self, use_case: InterfaceGeneratePaymentUseCase):
        self.__use_case = use_case
    
    async def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            amount = http_request.body.get("amount")
            desc = http_request.body.get("desc")
            email = http_request.body.get("email")
            schedule_id = http_request.body.get("schedule_id")
            
            if not all([amount, desc, email, schedule_id]):
                raise ValidationError("Missing required fields: amount, desc, email, schedule_id")
            
            if amount <= 0:
                raise ValidationError("Amount must be greater than zero", field="amount")

            response = await self.__use_case.payment(amount, desc, email, schedule_id)

            return HttpResponse(
                status_code=200,
                body = {
                    "data": response
                }
            )
        
        except Exception as error:
            return handle_errors(error)