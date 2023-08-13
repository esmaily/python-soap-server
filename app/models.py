from sqlalchemy import Integer, String, Column, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, backref

from datetime import datetime

BaseModel = declarative_base()


class ServiceModel(BaseModel):
    __tablename__ = 'services'
    """
       Represents a service provided by the customer.

       This class defines a data model for services and provides methods to interact with and
       manipulate service information.

       Attributes:
           id (int): The unique identifier for the service.
           customer_id (int): The ID of the customer associated with this service.
           name (str): The name of the service.
           number (str): The service number.
           created_on (datetime): The timestamp when the service was created.
           updated_on (datetime): The timestamp when the service was last updated.

       Methods:
           __repr__(): Returns a string representation of the service, including its ID and name.
           to_dict(): Converts the service data to a dictionary format.

    """

    def __repr__(self):
        return f"{self.id}"

    id = Column(Integer(), primary_key=True)
    customer_id = Column(Integer(), ForeignKey('customers.id'))
    name = Column(String(100), nullable=False)
    number = Column(String(12), nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    def to_dict(self) -> dict:
        """
           Convert the service sqlalchemy object to a dictionary.

           Returns:
             dict: A dictionary containing the service data.
        """
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "name": self.name,
            "number": self.number,
            "created_on": self.created_on.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_on": self.updated_on.strftime("%Y-%m-%d %H:%M:%S"),
        }


class CustomerModel(BaseModel):
    __tablename__ = 'customers'
    """
       Represents a customer's information.

       This class defines a data model for customers and provides methods to interact with and
       manipulate customer information.

       Attributes:
           id (int): The unique identifier for the customer.
           name (str): The name of the customer.
           family (str): The family name of the customer.
           national_code (str): The national code of the customer.
           father_name (str): The name of the customer's father.
           certificate_number (str): The certificate number of the customer.
           birthday (datetime): The birthday of the customer.
           address (str): The address of the customer.
           services (list): A list of services associated with the customer.
           created_on (datetime): The timestamp when the customer was created.
           updated_on (datetime): The timestamp when the customer was last updated.

       Methods:
           __repr__(): Returns a string representation of the customer, including its ID.
           to_dict(): Converts the customer data to a dictionary format.

    """
    def __repr__(self):
        """
            Get a string representation of the customer.

            Returns:
               str: A string in the format "id:{id}" representing the customer.
        """
        return f"id:{self.id}"

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

    def to_dict(self) -> dict:
        """
            Convert the service sqlalchemy object to a dictionary.

            Returns:
                dict: A dictionary containing the service data.
         """
        return {
            "id": self.id,
            "name": self.name,
            "family": self.family,
            "national_code": self.national_code,
            "father_name": self.father_name,
            "certificate_number": self.certificate_number,
            "birthday": self.birthday.strftime("%Y-%m-%d"),
            "address": self.address,
            "services": self.services,
            "created_on": self.created_on.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_on": self.updated_on.strftime("%Y-%m-%d %H:%M:%S"),
        }
