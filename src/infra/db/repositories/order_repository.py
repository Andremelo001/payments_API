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
        async for session in db_connection_handler.get_session():
            try:
                new_order = Order(
                    id= str(uuid4()),
                    id_schedule = schedule_id,
                    status_payment = str(status),
                    date_payment=date.today()
                )

                session.add(new_order)
                await session.commit()
                await session.refresh(new_order)

            except Exception as exception:
                await session.rollback()
                raise exception  

    async def update_status_payment(self, new_status: str, schedule_id: str) -> None:
        async for session in db_connection_handler.get_session():
                try:
                    payment = (await session.execute(select(Order).where(Order.id_schedule == schedule_id))).scalar_one_or_none()
                    
                    if not payment:
                        raise PaymentNotFoundError(schedule_id, "schedule_id")

                    payment.status_payment = new_status

                    await session.commit()
                
                except PaymentNotFoundError:
                    raise
                except Exception as exception:
                    await session.rollback()
                    raise exception
                
    async def get_payment(self, schedule_id: str) -> OrderModel:
        async for session in db_connection_handler.get_session():
                try:
                    payment = (await session.execute(select(Order).where(Order.id_schedule == schedule_id))).scalar_one_or_none()

                    return payment

                except Exception as exception:
                    raise exception