import json

from .models import CustomerModel, ServiceModel


class CustomerRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def get_all(self, order_by="ASK") -> list:
        with open(self.db_path) as json_file:
            data = json.load(json_file)
            customers = list(map(lambda item: CustomerModel(**item), data["customers"]))
            for itr in customers:
                itr.services = list(map(lambda item: ServiceModel(**item), itr.services))

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
        cm = CustomerModel(**customer)
        cm.services = list(map(lambda item: ServiceModel(**item), customer["services"]))
        return cm

    def store(self, customer: dict) -> object:
        data = self.__raw_get_all()
        customer["uid"] = len(data["customers"]) + 1
        data["customers"].append(customer)
        with open(self.db_path, 'w') as outfile:
            json.dump(data, outfile)

        return CustomerModel(**customer)


class ServiceRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def get_all(self, order_by="ASK") -> list:
        with open(self.db_path) as json_file:
            data = json.load(json_file)
            services = list(map(lambda item: ServiceModel(**item), data["services"]))
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
        services = list(map(lambda item: ServiceModel(**item), customer["services"]))
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

        return ServiceModel(**service)
