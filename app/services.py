from spyne import Array, ServiceBase, Unicode, rpc, Iterable

from app.validations import CustomerCreateValidation, ServiceCreateValidation

# from .models import CustomerModel, ServiceModel
from .repository import CustomerRepository, ServiceRepository

FILEPATH = "db.json"

customer_repo = CustomerRepository(FILEPATH)
service_repo = ServiceRepository(FILEPATH)
from app.schemas import CustomerSchema, ServiceSchema


class CustomerService(ServiceBase):
    def __init__(ctx):
        pass

    @rpc(Unicode(values=["ASC", "DESC"]), _returns=Array(CustomerSchema))
    def customer_get_list(ctx, order_by="ASC"):
        """Docstrings for customer service in the wsdl.

        @return the completed array
        """

        items = customer_repo.get_all(order_by)
        return items

    @rpc(Unicode, _returns=CustomerSchema)
    def customer_get(ctx, customer_id):
        """Docstrings for customer item in the wsdl.


        @return the completed customer object
        """

        customer = customer_repo.get_by_id(int(customer_id))

        return customer

        # yield u'ds'

    @rpc(Unicode(), Unicode, Unicode(max_len=10), Unicode, Unicode, Unicode, Unicode, _returns=CustomerSchema)
    def customer_create(ctx, name, family, national_code, father_name, certificate_number, birthday, address):
        """Docstrings for create customer   in the wsdl.

            @param name the customer name
            @param family the customer family
            @param national_code the customer national_code
            @param father_name the customer father_name
            @param certificate_number the customer card_number
            @param birthday the customer birthday
            @param address the customer address

            @return the completed Customer Object
         """

        payload = {
            "name": name,
            "family": family,
            "national_code": national_code,
            "father_name": father_name,
            "certificate_number": certificate_number,
            "birthday": birthday,
            "address": address,
            "services": []
        }

        validator = CustomerCreateValidation()
        validator.is_valid(payload)
        customer = customer_repo.store(payload)
        return customer

    @rpc(Unicode, _returns=Array(Iterable(Unicode)))
    def customer_get_service_list(ctx, customer_id):
        """Docstrings for customer services list by id in the wsdl.

        @return the completed array
        """

        items = service_repo.get_service_by_customer(customer_id)
        return items

    @rpc(Unicode, Unicode(max_len=150), Unicode(max_len=11), _returns=Iterable(Unicode))
    def customer_create_service(ctx, customer_id, name, number):
        """Docstrings for customer services list by id in the wsdl.

            @param customer_id the service customer_id
            @param name the service name
            @param number the service number

        @return the completed array
        """
        payload = {
            "customer_id": customer_id,
            "name": name,
            "number": number
        }
        customer = customer_repo.get_by_id(int(customer_id))
        services = service_repo.get_service_by_customer(customer_id)
        validator = ServiceCreateValidation()
        validator.is_valid({
            "services": services,
            "customer": customer
        })
        service = service_repo.store(payload)
        return service
