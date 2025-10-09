from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator
from dotenv import load_dotenv

import os

load_dotenv()

class DBConnectionHandler:
    def __init__(self) -> None:        
        
        self.__connection_string = os.getenv("DATABASE_URL")

        self.engine = create_async_engine(self.__connection_string, echo=True)

        self.session = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

        self.base = declarative_base()

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session() as session:
            yield session

db_connection_handler = DBConnectionHandler()