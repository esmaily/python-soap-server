import json
from app.schemas import CustomerSchema, ServiceSchema
from app.models import CustomerModel, ServiceModel

from app.core.db import db


class CustomerRepository:
    def __init__(self):
        self.conn = db.get_driver(CustomerModel, CustomerSchema)

    def get_all(self, order_by: str = "ASC") -> list:
        customers = self.conn.get_all(order_by)
        for customer in customers:
            customer.services = list(map(lambda item: ServiceSchema(**item.to_dict()), customer.services))

        return customers

    def raw_get_all(self, order_by: str = "ASC"):
        customers = self.conn.raw_get_all(order_by)
        return customers

    def get_by_id(self, customer_id: int) -> object:
        customer = self.conn.get_by_id(customer_id)
        customer.services = list(map(lambda item: ServiceSchema(**item.to_dict()), customer.services))
        return customer

    def store(self, customer: dict) -> object:
        created_customer = self.conn.store(customer)
        return created_customer

    def update(self, customer_id: int, customer: dict) -> object:
        updated_customer = self.conn.update(customer_id, customer)
        return updated_customer

    def delete(self, customer_id: int) -> object:
        self.conn.destroy(customer_id)
        return True


class ServiceRepository:
    def __init__(self):
        self.conn = db.get_driver(ServiceModel, ServiceSchema)

    def get_all(self, order_by: str = "ASC") -> list:
        services = self.conn.get_all(order_by)
        return services

    def raw_get_all(self, order_by: str = "ASC") -> dict:
        services = self.conn.raw_get_all(order_by)
        return services

    def get_by_customer(self, customer_id: int) -> list:
        services = self.conn.get_by(customer_id=customer_id)
        return services

    def get_by_id(self, service_id: int) -> object:
        return self.conn.get_by_id(service_id)

    def store(self, customer: dict) -> object:
        created_customer = self.conn.store(customer)
        return created_customer

    def update(self, customer_id: int, customer: dict) -> object:
        updated_customer = self.conn.update(customer_id, customer)
        return updated_customer

    def delete(self, customer_id: int) -> object:
        self.conn.destroy(customer_id)
        return True
