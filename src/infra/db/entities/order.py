from sqlalchemy import Column, String, Date
from src.infra.db.settings.db_connection_handler import db_connection_handler

class Order(db_connection_handler.base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True)
    id_schedule = Column(String, nullable=False)
    status_payment = Column(String, nullable=False)
    date_payment = Column(Date, nullable=False)