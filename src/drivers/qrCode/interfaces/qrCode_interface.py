from abc import ABC, abstractmethod
from typing import Dict

class qrCodeInterface(ABC):

    @abstractmethod
    def create_payment_pix(self, amount: int, desc: str, email: str, cpf: str) -> Dict: pass