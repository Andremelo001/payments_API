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
    
    def create_payment_pix(self, amount: float, desc: str, email: str, cpf: str) -> Dict:

        payment_data = {
            "transaction_amount": amount,
            "description": desc,
            "payment_method_id": 'pix',
            "payer": {
                "email": email,
                "identification": {
                    "type": "CPF",
                    "number": cpf
                },
            }
        }

        result = self.__sdk.payment().create(payment_data)

        payment = result["response"]

        return payment

qr_code = qrCode()