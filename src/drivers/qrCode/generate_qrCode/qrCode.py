import mercadopago
from dotenv import load_dotenv
import os
from typing import Dict, Optional

from src.drivers.qrCode.interfaces.qrCode_interface import qrCodeInterface

load_dotenv()

class qrCode(qrCodeInterface):
    def __init__(self):

        self.__acces_token = os.getenv("MERCADOPAGO_ACCESS_TOKEN")

        self.__sdk = mercadopago.SDK(self.__acces_token)
    
    def create_payment_pix(self, amount: float, desc: str, email: str, schedule_id: str) -> Dict:

        payment_data = {
            "transaction_amount": amount,
            "description": desc,
            "payment_method_id": 'pix',
            "external_reference": str(schedule_id),
            "payer": {
                "email": email,
            }
        }

        result = self.__sdk.payment().create(payment_data)

        payment = result["response"]

        return {
            "status": payment["status"],
            "qr_code": payment["point_of_interaction"]["transaction_data"]["qr_code"],
            "qr_code_base64": payment["point_of_interaction"]["transaction_data"]["qr_code_base64"],
            "ticket_url": payment["point_of_interaction"]["transaction_data"]["ticket_url"]
        }
    
    def get_payment_info(self, payment_id: str) -> Optional[Dict]:
        """
        Consulta o Mercado Pago para buscar o status atual do pagamento.
        Esse método deve ser chamado pelo Webhook.
        """

        result = self.__sdk.payment().get(payment_id)
        response = result.get("response")

        if not response:
            return None

        return {
            "id": response.get("id"),
            "status": response.get("status"),
            "status_detail": response.get("status_detail"),
            "external_reference": response.get("external_reference"),
            "payment_type_id": response.get("payment_type_id"),
            "transaction_amount": response.get("transaction_amount"),
            "date_approved": response.get("date_approved"),
        }