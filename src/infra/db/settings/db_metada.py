from sqlalchemy.ext.asyncio import AsyncEngine
from src.infra.db.settings.db_connection_handler import db_connection_handler

from src.infra.db.entities.order import Order

# Criar tabelas no banco de dados (assíncrono)
async def create_db_and_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(db_connection_handler.base.metadata.create_all)

async def init_db():
    await create_db_and_tables(db_connection_handler.engine)