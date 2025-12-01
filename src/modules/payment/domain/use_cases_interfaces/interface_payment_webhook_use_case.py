from abc import ABC, abstractmethod
from typing import Dict

class InterfacePaymentHebhookUseCase(ABC):

    @abstractmethod
    async def process_webhook(self, payment_id: str) -> Dict: pass