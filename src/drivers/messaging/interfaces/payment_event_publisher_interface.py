# src/drivers/messaging/interfaces/payment_event_publisher_interface.py
from abc import ABC, abstractmethod
from typing import Dict

class PaymentEventPublisherInterface(ABC):
    @abstractmethod
    async def publish_payment_event(self, event: Dict) -> None: pass
