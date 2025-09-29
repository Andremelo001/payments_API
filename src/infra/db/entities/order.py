from sqlalchemy import Column, Integer, String, Date
from src.infra.db.settings.db_connection_handler import db_connection_handler

class Order(db_connection_handler.base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_schedule = Column(String(100), nullable=False)
    date_payment = Column(Date, unique=True, nullable=False)