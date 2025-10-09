from sqlalchemy import Column, Integer, String, Date
from src.infra.db.settings.db_connection_handler import db_connection_handler

class Order(db_connection_handler.base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True)
    status_payment = Column(String, nullable=False)
    date_payment = Column(Date, nullable=False)