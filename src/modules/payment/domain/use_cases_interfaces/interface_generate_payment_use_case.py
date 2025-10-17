from abc import ABC, abstractmethod
from typing import Dict

class InterfaceGeneratePaymentUseCase(ABC):

    @abstractmethod
    async def payment(self, amount: float, desc: str, email: str) -> Dict: pass