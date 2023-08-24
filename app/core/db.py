import os
from decouple import Config, RepositoryEnv
from app.core.patterns import Singleton
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from app.models import BaseModel


env = Config(RepositoryEnv(f"{os.path.abspath(os.path.dirname(__name__))}/.env"))


class Database(metaclass=Singleton):

    def __init__(self):
        print("call init")
        self.__init_session = None
        self.engine = None

        self.db_url = URL.create(
            drivername=env.get("DB_DRIVER"),
            username=env.get("DB_USER"),
            password=env.get("DB_PASS"),
            host=env.get("DB_HOST"),
            database=env.get("DB_NAME")
        )
        self.connect()

    def connect(self):
        if self.__init_session:
            return self.__init_session
        self.engine = create_engine(self.db_url)
        session_object = sessionmaker(bind=self.engine)
        BaseModel.metadata.create_all(self.engine)
        self.__init_session = session_object()

    def get_session(self):
        return self.__init_session


db = Database()
session = db.get_session()
