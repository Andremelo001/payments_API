from abc import ABC, abstractmethod
from typing import Dict

class InterfaceGetPaymentUseCase(ABC):

    @abstractmethod
    async def get_payment(self, schedule_id: str) -> Dict: pass