import mercadopago
from dotenv import load_dotenv
import os
from typing import Dict, Optional
import httpx

from src.drivers.qrCode.interfaces.qrCode_interface import qrCodeInterface

load_dotenv()

class qrCode(qrCodeInterface):
    def __init__(self):

        self.__acces_token = os.getenv("MERCADOPAGO_ACCESS_TOKEN")

        self.__base_url = "https://api.mercadopago.com/v1/payments"

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
    
    async def get_payment_info(self, payment_id: str) -> Optional[Dict]:
        """
        Consulta o Mercado Pago de forma assíncrona para buscar o status atual do pagamento.
        Esse método é utilizado pelo Webhook.
        """

        url = f"{self.__base_url}/{payment_id}"
        headers = {
            "Authorization": f"Bearer {self.__acces_token}",
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient(timeout=20.0) as client:
            try:
                response = await client.get(url, headers=headers)

                if response.status_code == 404:
                    return None

                response.raise_for_status()
                data = response.json()

                return {
                    "id": data.get("id"),
                    "status": data.get("status"),
                    "status_detail": data.get("status_detail"),
                    "external_reference": data.get("external_reference"),
                    "payment_type_id": data.get("payment_type_id"),
                    "transaction_amount": data.get("transaction_amount"),
                    "date_approved": data.get("date_approved"),
                }

            except httpx.HTTPStatusError as e:
                print(f"Erro Mercado Pago: {e.response.text}")
                return None

            except Exception as e:
                print(f"Erro inesperado ao consultar pagamento: {e}")
                return None