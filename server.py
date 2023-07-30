#!/usr/bin/env python


"""
This is a simple Shatel mobile  example to show the basics of writing
a webservice using spyne, starting a server, and creating a service
client.


"""


from spyne import Application, rpc,Mandatory as M, ServiceBase,Array, Iterable, Integer, Unicode,String,TTableModel, Service, ResourceNotFoundError, UnsignedInteger32
from spyne.util import memoize
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

from sqlalchemy import MetaData, create_engine

from sqlalchemy.orm import sessionmaker

class CustomerService(ServiceBase):
    @rpc(String, String, _returns=Iterable(Unicode))
    def customer_create(ctx, name, family):
        """Docstrings for service methods appear as documentation in the wsdl.

        @param name the customer name
        @param family the customer family
        @param national_code the customer national_code
        @param father_name the customer father_name
        @param certificate_number the customer card_number
        @param bithday the customer birthday
        @param address the customer address
        @return the completed True
        """

        
        yield u'Hello, %s  ' % name+family

    def customer_list(ctx):
        """Docstrings for service methods appear as documentation in the wsdl.

        @return the completed array
        """


        yield u'custoemr list, %s'









application = Application([CustomerService], 'spyne.examples.hello.soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())


wsgi_application = WsgiApplication(application)


if __name__ == '__main__':
    import logging

    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

    logging.info("listening to http://127.0.0.1:8000")
    logging.info("wsdl is at: http://localhost:8000/?wsdl")



    server = make_server('0.0.0.0', 8000, wsgi_application)
    server.serve_forever()

