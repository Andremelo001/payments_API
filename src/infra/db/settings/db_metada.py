from src.infra.db.settings.db_connection_handler import db_connection_handler
from src.infra.db.entities.order import Order

db_connection_handler.base.metadata.create_all(db_connection_handler.engine())