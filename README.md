# Python Simple Soap Server

  
License: MIT


### Setup Project

Create virtual env:

    $ python -m venv .venv
    $ source .venv/bin/activate
    $ pip install -r requirements.txt

Run project :

     $ python server.py
  

Sample params for  customer create :

url: `http://localhost:8000/?wsdl` <br />
**Soap request params: <br />**
`<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
          <soap:Body>
            <customer_create xmlns="spyne.examples.hello.soap">
                <name>Jafar</name>
                <family>Esmaili</family>
            </customer_create>
          </soap:Body>
</soap:Envelope>
`      
      
**Soap response:<br />**
`<?xml version='1.0' encoding='UTF-8'?>
<soap11env:Envelope xmlns:soap11env="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="spyne.examples.hello.soap">
    <soap11env:Body>
        <tns:customer_createResponse>
            <tns:customer_createResult>
                <tns:string>Hello, Jafar  Esmaili</tns:string>
            </tns:customer_createResult>
        </tns:customer_createResponse>
    </soap11env:Body>
</soap11env:Envelope>`

> If you import database this step is not needed
 
 


 