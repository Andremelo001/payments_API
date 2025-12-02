from src.modules.payment.data.interfaces.interface_payment_repository import InterfacePaymentRepository
from src.infra.db.settings.db_connection_handler import db_connection_handler
from src.infra.db.entities.order import Order
from src.modules.payment.domain.models.order import OrderModel
from src.errors import PaymentNotFoundError
from datetime import date
from uuid import uuid4
from sqlalchemy import select

class OrderRepository(InterfacePaymentRepository):
    async def generate_payment(self, status: str, schedule_id: str) -> None:
        async with db_connection_handler.get_session() as session:
            new_order = Order(
                id= str(uuid4()),
                id_schedule = schedule_id,
                status_payment = str(status),
                date_payment=date.today()
            )

            session.add(new_order)
            await session.flush()
            await session.refresh(new_order)  

    async def update_status_payment(self, new_status: str, schedule_id: str) -> None:
        async with db_connection_handler.get_session() as session:
            payment = (await session.execute(select(Order).where(Order.id_schedule == schedule_id))).scalar_one_or_none()
            
            if not payment:
                raise PaymentNotFoundError(schedule_id, "schedule_id")

            payment.status_payment = new_status
                
    async def get_payment(self, schedule_id: str) -> OrderModel:
        async with db_connection_handler.get_session() as session:
            payment = (await session.execute(select(Order).where(Order.id_schedule == schedule_id))).scalar_one_or_none()
            return payment