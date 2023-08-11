from sqlalchemy import MetaData, Integer, String, Column, DateTime, Text, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, backref

from datetime import datetime

BaseModel = declarative_base()


class ServiceModel(BaseModel):
    __tablename__ = 'services'

    def __str__(self):
        return f"{self.id}-{self.name}"

    # def __
    id = Column(Integer(), primary_key=True)
    customer_id = Column(Integer(), ForeignKey('customers.id'))
    name = Column(String(100), nullable=False)
    number = Column(String(12), nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    # def fields(self):
    #     return self.


class CustomerModel(BaseModel):
    __tablename__ = 'customers'

    def __repr__(self):
        return f"id:{self.id}"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "family": self.family,
            "national_code": self.national_code,
            "father_name": self.father_name,
            "certificate_number": self.certificate_number,
            "birthday": self.birthday,
            "address": self.address,
            "services": self.services,
            "created_on": self.created_on,
            "updated_on": self.updated_on,
        }

    id = Column(Integer(), primary_key=True)
    name = Column(String(100), nullable=False)
    family = Column(String(100), nullable=False)
    national_code = Column(String(10), nullable=False)
    father_name = Column(String(100), nullable=False)
    certificate_number = Column(String(100), nullable=False)
    birthday = Column(DateTime(), nullable=True)
    address = Column(Text)
    services = relationship('ServiceModel', backref='customer')
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
