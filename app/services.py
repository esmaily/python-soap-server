from spyne import Application, rpc, ServiceBase, Iterable, Integer, Unicode
import json
from spyne.protocol.xml import XmlDocument
from spyne.server.http import HttpTransportContext
from .repository import CustomerRepository

FILEPATH = "db.json"
json_file = open(FILEPATH)
data = json.load(json_file)
json_file.close()
print(data)
from .repository import CustomerRepository


class CustomerService(ServiceBase):
    def __init__(ctx):
        print('callllllll---------')
        ctx.customerRepo = CustomerRepository(FILEPATH)
    @rpc(_returns=Iterable(Unicode) ,_body_style='bare')
    def customer_get_list(ctx):
        """Docstrings for service methods appear as documentation in the wsdl.

        @return the completed array
        """
        data = ctx.customerRepo.get_all()

        if isinstance(ctx.transport, HttpTransportContext):
            ctx.transport.set_mime_type("application/xml")
        print("is call")
        return data

    @rpc(Unicode, Unicode,Unicode,Unicode, _returns=Iterable(Unicode))
    def customer_create(ctx, name, family, national_code, father_name):
        """Docstrings for service methods appear as documentation in the wsdl.

        @return the completed array
        """

        customer = {
            "name": name,
            "family": family,
            "national_code": national_code,
            "father_name": father_name,
        }
        print(customer)
        customerRepo = CustomerRepository(FILEPATH)
        customerRepo.store(customer)
        yield u'customer has been created'
