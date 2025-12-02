from src.modules.payment.domain.use_cases_interfaces.interface_payment_webhook_use_case import InterfacePaymentHebhookUseCase
from src.presentation.interface.controller_interface import ControllerInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.errors import handle_errors, WebhookValidationError

class PaymentWebhookController(ControllerInterface):
    def __init__(self, use_case: InterfacePaymentHebhookUseCase):
        self.__use_case = use_case
    
    async def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            if "data" not in http_request.body or "id" not in http_request.body["data"]:
                raise WebhookValidationError("Invalid webhook payload structure")
            
            payment_id = http_request.body["data"]["id"]
            
            if not payment_id:
                raise WebhookValidationError("Missing payment_id in webhook data")
            
            # Extrai headers e delega validação para o use case
            x_signature = http_request.headers.get("x-signature", "")
            x_request_id = http_request.headers.get("x-request-id", "")
            
            response = await self.__use_case.process_webhook(
                payment_id=payment_id,
                x_signature=x_signature,
                x_request_id=x_request_id
            )

            return HttpResponse(
                status_code=200,
                body = {
                    "data": response
                }
            )
        
        except Exception as error:
            return handle_errors(error)