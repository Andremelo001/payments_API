import mercadopago
from dotenv import load_dotenv
import os
from typing import Dict

from src.drivers.qrCode.interfaces.qrCode_interface import qrCodeInterface

load_dotenv()

class qrCode(qrCodeInterface):
    def __init__(self):

        self.__acces_token = os.getenv("ACCESS_TOKEN")

        self.__sdk = mercadopago.SDK(self.__acces_token)
    
    def create_payment_pix(self, amount: int, desc: str, email: str, cpf: str) -> Dict:

        payment_data = {
            "transaction_amount": amount,
            "description": desc,
            "payment_method_id": 'pix',
            "payer": {
                "email": email,
                "identification": {
                    "type": cpf,
                }
            }
        }

        result = self.__sdk.payment().create(payment_data)

        payment = result["response"]

        return {
            "id": payment["id"],
            "status": payment["status"],
            "qr_code": payment["point_of_interaction"]["transaction_data"]["qr_code"],
            "qr_code_base64": payment["point_of_interaction"]["transaction_data"]["qr_code_base64"],
            "ticket_url": payment["point_of_interaction"]["transaction_data"]["ticket_url"]
        }