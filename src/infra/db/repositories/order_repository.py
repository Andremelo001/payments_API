from src.modules.payment.data.interfaces.interface_payment_repository import InterfacePaymentRepository
from src.infra.db.settings.db_connection_handler import db_connection_handler
from src.infra.db.entities.order import Order
from datetime import date
from uuid import uuid4

class OrderRepository(InterfacePaymentRepository):
    async def generate_payment(self, status: str) -> None:
        async for session in db_connection_handler.get_session():
            try:
                new_order = Order(
                    id= str(uuid4()),
                    status_payment = str(status),
                    date_payment=date.today()
                )

                session.add(new_order)
                await session.commit()
                await session.refresh(new_order)

            except Exception as exception:
                await session.rollback()
                raise exception



        
