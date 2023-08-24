from app.core.patterns import Singleton
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from app.models import BaseModel
import json
from app.core.config import settings
from sqlalchemy import update, delete
from app.core.patterns import Orm


class Database(metaclass=Singleton):

    def __init__(self):
        self.__init_connection = None
        self.engine = None
        self.json_db_file = settings.JSON_DB_FILE
        self.postgres_url = URL.create(
            drivername=settings.DB_CONNECTION_DRIVER,
            username=settings.DB_USER,
            password=settings.DB_PASS,
            host=settings.DB_HOST,
            database=settings.DB_NAME
        )

    def postgres_connect(self):
        if self.__init_connection:
            return self.__init_connection
        self.engine = create_engine(self.postgres_url)
        session_object = sessionmaker(bind=self.engine)
        BaseModel.metadata.create_all(self.engine)
        self.__init_connection = session_object()

    def get_connection(self):
        return self.__init_connection

    def get_driver(self, orm_model, orm_schema):
        if settings.STORAGE_TYPE == "json":
            return JsonDB(orm_model, orm_schema)
        elif settings.STORAGE_TYPE == "postgres":
            self.postgres_connect()
            return PostgresDB(orm_model, orm_schema)
        else:
            raise "please set database connection driver"


db = Database()


class JsonDB(Orm):

    def __init__(self, model, schema):
        self.db_path: str = settings.JSON_DB_FILE
        self.model = model
        self.schema = schema

    def get_all(self, order_by="ASK") -> list:
        with open(self.db_path) as json_file:
            data = json.load(json_file)
            customers = list(map(lambda item: self.schema(**item), data["customers"]))
            for itr in customers:
                itr.services = list(map(lambda item: self.schema(**item), itr.services))

        if order_by == "DESC":
            customers.reverse()
        return customers

    def raw_get_all(self):
        with open(self.db_path) as json_file:
            data = json.load(json_file)
        return data

    def get_by_id(self, customer_id: int) -> object:
        data = self.__raw_get_all()
        indices = [index for (index, item) in enumerate(data["customers"]) if item["uid"] == int(customer_id)]
        if not indices:
            return None
        customer = data["customers"][indices[0]]
        cm = self.schema(**customer)
        cm.services = list(map(lambda item: self.schema(**item), customer["services"]))
        return cm

    def get_by(self, **kwargs):
        pass

    def store(self, customer: dict) -> object:
        data = self.__raw_get_all()
        customer["uid"] = len(data["customers"]) + 1
        data["customers"].append(customer)
        with open(self.db_path, 'w') as outfile:
            json.dump(data, outfile)

        return self.schema(**customer)

    def update(self, model_id: int, data: dict):
        pass

    def destroy(self, model_id: int):
        pass


class PostgresDB(Orm):

    def __init__(self, model, schema):
        self.model = model
        self.schema = schema
        self.session = db.get_connection()

    def get_all(self, order_by: str):
        order_by = self.model.id.desc() if order_by == 'DESC' else self.model.id.asc()
        items = self.session.query(self.model).order_by(order_by)
        serialized = list(map(lambda item: self.schema(**item.to_dict()), items))

        return serialized

    def raw_get_all(self, order_by: str):
        order_by = self.model.id.desc() if order_by == 'DESC' else self.model.id.asc()
        items = self.session.query(self.model).order_by(order_by)

        return items

    def get_by_id(self, model_id: int):
        model_object = self.session.query(self.model).filter(self.model.id == model_id).first()
        return self.schema(**model_object.to_dict())

    def get_by(self, **kwargs):
        filters = list(map(lambda itr: getattr(self.model, itr) == kwargs[itr], kwargs))
        items = self.session.query(self.model).filter(*filters)
        items = list(map(lambda item: self.schema(**item.to_dict()), items))
        return items

    def store(self, data):
        new_model = self.model(**data)
        self.session.add(new_model)
        self.session.commit()

        return self.schema(**new_model.to_dict())

    def update(self, model_id: int, data: dict):
        query = update(self.model).where(self.model.id == model_id).values(data)
        self.session.execute(query)
        self.session.commit()

        return self.get_by_id(model_id)

    def destroy(self, model_id: int):
        query = delete(self.model).where(self.model.id == model_id)
        self.session.execute(query)
        self.session.commit()
        return True
