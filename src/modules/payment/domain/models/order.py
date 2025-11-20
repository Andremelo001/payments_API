from uuid import UUID
from datetime import date

class OrderModel():
    def __init__(self, id: UUID, id_schedule: str, status_payment: str, date_payment: date) -> None:
        self.id = id
        self.id_schedule = id_schedule
        self.status_payment = status_payment
        self.date_payment = date_payment