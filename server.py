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
from sqlalchemy.orm import registry
from sqlalchemy.orm import sessionmaker


"""

config database 

"""


db = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=db)
TableModel = TTableModel()
TableModel.Attributes.sqla_metadata.bind = db
metadata = MetaData()
# mapper_registry = registry(metadata=metadata)

class Service(TableModel):
    __tablename__ = 'services'
    __namespace__ = 'spyne.examples.sql_crud'
    __table_args__ = {"sqlite_autoincrement": True}
    # mapper_registry.metadata
    id = UnsignedInteger32(primary_key=True)
    name = Unicode(256)
    number = Unicode(256)

class Customer(TableModel):
    __tablename__ = 'customers'
    __namespace__ = 'spyne.examples.sql_crud'
    __table_args__ = {"sqlite_autoincrement": True}
    # mapper_registry.metadata
    id = UnsignedInteger32(primary_key=True)
    name = Unicode(256)
    first_name = Unicode(256)
    last_name = Unicode(256)
    national_code = Unicode(256)
    father_name = Unicode(256)
    certificate_number = Unicode(256)
    birthday = Unicode(256)
    address = Unicode(256)
    services = Array(Service, store_as='table')

class CustomerService(ServiceBase):
    @rpc(String, String, _returns=Iterable(Unicode))
    def customer_create(ctx, name, family):
        """Docstrings for service methods appear as documentation in the wsdl.
        <b>What fun!</b>

        @param name the customer name
        @param family the customer family
        @param national_code the customer national_code
        @param father_name the customer father_name
        @param certificate_number the customer card_number
        @param bithday the customer birthday
        @param address the customer address
        @return the completed True
        """
        print({name,family})
        
        yield u'Hello, %s , %s' % name % family

    def customer_list(ctx, name, times):
        """Docstrings for service methods appear as documentation in the wsdl.
        <b>What fun!</b>

        @param name the name to say hello to
        @param times the number of times to say hello
        @return the completed array
        """

        for i in range(times):
            yield u'Hello, %s' % name



@memoize
def TCrudService(T, T_name):
    class CrudService(Service):
        @rpc(M(UnsignedInteger32, _returns=T))
        def get(ctx, obj_id):
            return ctx.udc.session.query(T).filter_by(id=obj_id).one()

        @rpc(T, _returns=UnsignedInteger32)
        def put(ctx, obj):
            if obj.id is None:
                ctx.udc.session.add(obj)
                ctx.udc.session.flush()

            else:
                if ctx.udc.session.query(T).get(obj.id) is None:
                    raise ResourceNotFoundError('%s.id=%d' % (T_name, obj.id))

                else:
                    ctx.udc.session.merge(obj)

            return obj.id

        @rpc(M(UnsignedInteger32))
        def del_(ctx, obj_id):
            count = ctx.udc.session.query(T).filter_by(id=obj_id).count()
            if count == 0:
                raise ResourceNotFoundError(obj_id)

            ctx.udc.session.query(T).filter_by(id=obj_id).delete()

        @rpc(_returns=Iterable(T))
        def get_all(ctx):
            return ctx.udc.session.query(T)

    return CrudService


class CustomerDefinedContext(object):
    def __init__(self):
        self.session = Session()


def _on_method_call(ctx):
    ctx.udc = CustomerDefinedContext()


def _on_method_return_object(ctx):
    ctx.udc.session.commit()


def _on_method_context_closed(ctx):
    if ctx.udc is not None:
        ctx.udc.session.close()


customer_service = TCrudService(Customer, 'customer')



application = Application([CustomerService], 'spyne.examples.hello.soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())
application.event_manager.add_listener('method_call', _on_method_call)
application.event_manager.add_listener('method_return_object',
                                                      _on_method_return_object)
application.event_manager.add_listener("method_context_closed",
                                                      _on_method_context_closed)

wsgi_application = WsgiApplication(application)


if __name__ == '__main__':
    import logging

    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

    logging.info("listening to http://127.0.0.1:8000")
    logging.info("wsdl is at: http://localhost:8000/?wsdl")

    TableModel.Attributes.sqla_metadata.create_all()

    server = make_server('0.0.0.0', 8000, wsgi_application)
    server.serve_forever()

