from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from dotenv import load_dotenv
import os

load_dotenv()

class DBConnectionHandler:
    def __init__(self) -> None:        
        self.__connection_string = os.getenv("DATABASE_URL")
        self.engine = create_async_engine(self.__connection_string, echo=True)
        self.session_factory = async_sessionmaker(
            self.engine, 
            class_=AsyncSession, 
            expire_on_commit=False
        )
        self.base = declarative_base()

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Context manager para sessões do banco."""
        session = self.session_factory()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

db_connection_handler = DBConnectionHandler()