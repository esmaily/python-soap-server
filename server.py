#!/usr/bin/env python


"""
This is a simple Python soap server  example to show the basics of writing
a webservice using spyne, starting a server, and creating a service
client.

"""

from spyne import Application, ResourceNotFoundError
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

from app.controllers import CustomerController, ServiceController

application = Application([CustomerController, ServiceController], 'python.soap.example',
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
