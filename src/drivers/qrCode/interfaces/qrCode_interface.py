from abc import ABC, abstractmethod
from typing import Dict, Optional

class qrCodeInterface(ABC):

    @abstractmethod
    def create_payment_pix(self, amount: int, desc: str, email: str, schedule_id: str) -> Dict: pass

    @abstractmethod
    async def get_payment_info(self, payment_id: str) -> Optional[Dict]: pass