from spyne import Array, ServiceBase, Unicode, rpc, Iterable

from app.validations import CustomerCreateValidation, ServiceCreateValidation

from .repository import CustomerRepository, ServiceRepository

customer_repo = CustomerRepository()
service_repo = ServiceRepository()
from app.schemas import CustomerSchema, ServiceSchema


class CustomerController(ServiceBase):

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

    @rpc(Unicode(), Unicode(), Unicode(), Unicode(), _returns=CustomerSchema)
    def customer_edit(ctx, customer_id, name, family, address):
        """Docstrings for create customer   in the wsdl.

            @param customer_id the customer id
            @param name the customer name
            @param family the customer family
            @param address the customer address

            @return the completed Customer Object
         """

        payload = {
            "name": name,
            "family": family,
            "address": address,
        }

        customer = customer_repo.update(customer_id, payload)

        return customer

    @rpc(Unicode(), _returns=CustomerSchema)
    def customer_delete(ctx, customer_id):
        """Docstrings for create customer   in the wsdl.

            @param customer_id the customer id
            @return the completed Customer Object
         """

        customer = customer_repo.delete(customer_id)

        return customer


class ServiceController(ServiceBase):

    @rpc(Unicode, Unicode(max_len=150), Unicode(max_len=11), _returns=ServiceSchema)
    def service_create(ctx, customer_id, name, number):
            """Docstrings for   service create.

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
            services = service_repo.get_by_customer(customer_id)
            validator = ServiceCreateValidation()
            validator.is_valid({
                "services": services,
                "customer": customer
            })
            new_service = service_repo.store(payload)
            return new_service
    @rpc(Unicode(values=["ASC", "DESC"]), _returns=Array(ServiceSchema))
    def service_get_list(ctx, order_by="ASC"):
        """Docstrings for  service list in the wsdl.

        @return the completed array
        """

        items = service_repo.get_all(order_by)
        return items

    @rpc(Unicode, _returns=ServiceSchema)
    def service_get(ctx, service_id):
        """Docstrings for service item in the wsdl.
        
        @param service_id the customer 

        @return the completed service object
        """

        service = service_repo.get_by_id(int(service_id))

        return service

    @rpc(Unicode(), Unicode(), Unicode, _returns=ServiceSchema)
    def service_edit(ctx, service_id, name, number):
        """Docstrings for edit service   in the wsdl.

            @param service_id the customer id
            @param name the customer name
            @param number the customer number

            @return the completed service Object
         """

        payload = {
            "name": name,
            "number": number,
        }

        service = service_repo.update(service_id, payload)

        return service

    @rpc(Unicode, _returns=Array(ServiceSchema))
    def customer_get_service_list(ctx, customer_id):
        """Docstrings for customer services list by id in the wsdl.

        @return the completed array
        """

        items = service_repo.get_by_customer(customer_id)
        return items

    @rpc(Unicode, _returns=ServiceSchema)
    def service_delete(ctx, service_id):
        """Docstrings for customer item in the wsdl.

        @param service_id the customer id

        @return the completed service object
        """
       
        service = service_repo.delete(int(service_id))

        return service

    
