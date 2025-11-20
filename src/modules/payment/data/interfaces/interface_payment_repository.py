from abc import ABC, abstractmethod
from src.modules.payment.domain.models.order import OrderModel

class InterfacePaymentRepository(ABC):

    @abstractmethod
    async def generate_payment(self, status: str, schedule_id: str) -> None: pass

    @abstractmethod
    async def update_status_payment(self, new_status: str, schedule_id: str) -> None: pass

    @abstractmethod
    async def get_payment(self, schedule_id: str) -> OrderModel: pass