from abc import ABC, abstractmethod

class NotifyApiInterface(ABC):

    @abstractmethod
    async def notify_main_api(self, schedule_id: str, status: str) -> bool: pass