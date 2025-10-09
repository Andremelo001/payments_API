from abc import ABC, abstractmethod

class InterfacePaymentRepository(ABC):

    @abstractmethod
    async def generate_payment(self, status: str) -> None: pass