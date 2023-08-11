from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from .models import BaseModel

"""

config database 

"""


class Database:

    def __init__(self):
        self.__init_session = None
        self.engine = None

        self.db_url = URL.create(
            drivername="postgresql",
            username="myuser",
            password="mypass",
            host="localhost",
            database="pysoap"
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
