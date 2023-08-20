import json
from abc import ABC
from app.schemas import CustomerSchema, ServiceSchema
from app.models import CustomerModel, ServiceModel
from app.db import session
from sqlalchemy import update, delete

class Storage(ABC):
    def get_all(self, order_by: str):
        pass

    def get_by_id(self, model_id: int):
        pass

    def create(self, model_id: int):
        pass

    def update(self, model_id: int, data: dict):
        pass

    def delete(self, model_id: int):
        pass


class JsonDB:
    def __init__(self, db_path: str):
        self.db_path: str = db_path

    def get_all(self, order_by="ASK") -> list:
        with open(self.db_path) as json_file:
            data = json.load(json_file)
            customers = list(map(lambda item: CustomerSchema(**item), data["customers"]))
            for itr in customers:
                itr.services = list(map(lambda item: ServiceSchema(**item), itr.services))

        if order_by == "DESC":
            customers.reverse()
        return customers

    def __raw_get_all(self):
        with open(self.db_path) as json_file:
            data = json.load(json_file)
        return data

    def get_by_id(self, customer_id: int) -> object:
        data = self.__raw_get_all()
        indices = [index for (index, item) in enumerate(data["customers"]) if item["uid"] == int(customer_id)]
        if not indices:
            return None
        customer = data["customers"][indices[0]]
        cm = CustomerSchema(**customer)
        cm.services = list(map(lambda item: ServiceSchema(**item), customer["services"]))
        return cm

    def store(self, customer: dict) -> object:
        data = self.__raw_get_all()
        customer["uid"] = len(data["customers"]) + 1
        data["customers"].append(customer)
        with open(self.db_path, 'w') as outfile:
            json.dump(data, outfile)

        return CustomerSchema(**customer)


class PostgresDB:
    def __init__(self, model: [CustomerModel], schema: [CustomerSchema]):
        self.model = model
        self.schema = schema

    def get_all(self, order_by: str):
        order_by = self.model.id.desc() if order_by == 'DESC' else self.model.id.asc()
        items = session.query(self.model).order_by(order_by)
        serialized = list(map(lambda item: self.schema(**item.to_dict()), items))

        return serialized

    def __raw_get_all(self, order_by: str):
        order_by = self.model.id.desc() if order_by == 'DESC' else self.model.id.asc()
        items = session.query(self.model).order_by(order_by)

        return items

    def get_by_id(self, model_id: int):
        model_object = session.query(self.model).filter(self.model.id == model_id).first()
        return CustomerSchema(**model_object.to_dict())

    def store(self, data):
        new_model = self.model(**data)
        session.add(new_model)
        session.commit()

        return CustomerSchema(**new_model.to_dict())

    def update(self, model_id: int, data: dict):
        query = update(self.model).where(self.model.id == model_id).values(data)
        session.execute(query)
        session.commit()

        return self.get_by_id(model_id)

    def delete(self, model_id: int):
        query = delete(self.model).where(self.model.id == model_id)
        session.execute(query)
        session.commit()
        return True


class CustomerRepository:
    def __init__(self, db_path: str):
        self.db_path: str = db_path
        self.conn = PostgresDB(CustomerModel, CustomerSchema)

    def get_all(self, order_by="ASC") -> list:
        items = self.conn.get_all(order_by)
        return items

    def __raw_get_all(self):
        with open(self.db_path) as json_file:
            data = json.load(json_file)
        return data

    def get_by_id(self, customer_id: int) -> object:
        return self.conn.get_by_id(customer_id)

    def store(self, customer: dict) -> object:
        created_customer = self.conn.store(customer)
        return CustomerSchema(**created_customer.to_dict())

    def update(self, customer_id: int, customer: dict) -> object:
        updated_customer = self.conn.update(customer_id, customer)
        return updated_customer

    def delete(self, customer_id: int) -> object:
        self.conn.delete(customer_id)
        return True


class ServiceRepository:
    def __init__(self, db_path: str):
        self.db_path: str = db_path

    def get_all(self, order_by="ASK") -> list:
        with open(self.db_path) as json_file:
            data = json.load(json_file)
            services = list(map(lambda item: ServiceSchema(**item), data["services"]))
        if order_by == "DESC":
            services.reverse()
        return services

    def _raw_get_all(self) -> dict:
        with open(self.db_path) as json_file:
            data = json.load(json_file)
        return data

    def get_service_by_customer(self, customer_id: int) -> list:
        data = self._raw_get_all()
        indices = [index for (index, item) in enumerate(data["customers"]) if item["uid"] == int(customer_id)]
        if not indices:
            return []
        customer = data["customers"][indices[0]]
        services = list(map(lambda item: ServiceSchema(**item), customer["services"]))
        return services

    def store(self, service: dict) -> object:
        data = self._raw_get_all()
        indices = [index for (index, item) in enumerate(data["customers"]) if
                   item["uid"] == int(service["customer_id"])]
        if not indices:
            return False
        customer = data["customers"][indices[0]]
        service["uid"] = len(customer["services"]) + 1
        customer["services"].append(service)
        data["customers"][indices[0]] = customer
        with open(self.db_path, 'w') as outfile:
            json.dump(data, outfile)

        return ServiceSchema(**service)
