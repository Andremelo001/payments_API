from dotenv import load_dotenv
import os
import httpx

from src.drivers.notify_api.interfaces.notify_api_interface import NotifyApiInterface

load_dotenv()

class NotifyApi(NotifyApiInterface):
    def __init__(self):
        self.__api_main_url = (
            os.getenv("API_MAIN_URL_PRODUCTION") or 
            os.getenv("API_MAIN_URL_DEVELOPMENT")
        )
    
    async def notify_main_api(self, schedule_id: str, status: str) -> bool:
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    f"{self.__api_main_url}/clients/notification",
                    json={
                        "schedule_id": schedule_id,
                        "status": status
                    },
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                return True
            
            except Exception as e:
                print(f"Erro ao notificar API principal: {e}")
                return False
