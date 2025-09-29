from databases import Database
import sqlalchemy
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

class DBConnectionHandler:
    def __init__(self) -> None:        
        
        self.__connection_string = os.getenv("DATABASE_URL")

        self.__database = Database(self.__connection_string)

        self.base = declarative_base()

    async def connect_to_db(self):
        await self.__database.connect()

    async def disconnect_to_db(self):
        await self.__database.disconnect()

    def get_db_conn(self):
        return self.__database
    
    def engine(self):
        return sqlalchemy.create_engine(self.__connection_string)

db_connection_handler = DBConnectionHandler()