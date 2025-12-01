from src.modules.payment.domain.use_cases_interfaces.interface_get_payment_use_case import InterfaceGetPaymentUseCase
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.errors import handle_errors, ValidationError

class GetPaymentController(ControllerInterface):
    def __init__(self, use_case: InterfaceGetPaymentUseCase):
        self.__use_case = use_case
    
    async def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            id_schedule = http_request.query_params.get("id_schedule")
            
            if not id_schedule:
                raise ValidationError("Missing required parameter: id_schedule", field="id_schedule")

            response = await self.__use_case.get_payment(id_schedule)

            return HttpResponse(
                status_code=200,
                body = {
                    "data": response
                }
            )
        
        except Exception as error:
            return handle_errors(error)