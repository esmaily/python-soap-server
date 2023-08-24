from spyne import ComplexModel, Unicode, UnsignedInteger32, Iterable
from dataclasses import dataclass


@dataclass
class ServiceSchema(ComplexModel):
    id: int = UnsignedInteger32(pk=True)
    name: str = Unicode(150)
    number: int = UnsignedInteger32()
    customer_id: int = UnsignedInteger32()
    created_on: str = Unicode(250)
    updated_on: str = Unicode(250)

    def __init__(self, id: int, name: str, number: int, customer_id: int, created_on: str = None,
                 updated_on: str = None):
        self.id = id
        self.name = name
        self.number = number
        self.customer_id = customer_id
        self.created_on = created_on
        self.updated_on = updated_on


@dataclass
class CustomerSchema(ComplexModel):
    id: int = UnsignedInteger32(pk=True)
    name: str = Unicode(150, min_len=4, pattern='[a-z0-9.]+')
    family: str = Unicode(150)
    national_code: str = Unicode(10)
    father_name: str = Unicode(150)
    certificate_number: int = Unicode(10)
    birthday: str = Unicode(15)
    address: str = Unicode(250)
    services: list = Iterable(ServiceSchema)
    created_on: str = Unicode(250)
    updated_on: str = Unicode(250)

    def __init__(self, id: int, name: str, family: str, national_code: str, father_name: str, certificate_number: int,
                 birthday: str, address: str, services: list, created_on: str = None, updated_on: str = None):
        self.id = id
        self.name = name
        self.family = family
        self.national_code = national_code
        self.father_name = father_name
        self.certificate_number = certificate_number
        self.birthday = birthday
        self.address = address
        self.services = services
        self.created_on = created_on
        self.updated_on = updated_on
