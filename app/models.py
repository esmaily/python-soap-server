from spyne import Unicode, ComplexModel, UnsignedInteger32
from spyne.model.complex import ComplexModelBase, ComplexModelMeta, Array, Iterable
from sqlalchemy import MetaData


class TableModel(ComplexModelBase):
    __metaclass__ = ComplexModelMeta
    __metadata__ = MetaData()


class ServiceModel(ComplexModel):
    uid = UnsignedInteger32(pk=True)
    name = Unicode(150)
    number = Unicode(200)
    customer_id = Unicode(200)

    def __init__(self, uid, name, number, customer_id):
        self.uid = uid
        self.name = name
        self.number = number
        self.customer_id = customer_id


class CustomerModel(ComplexModel):
    uid = UnsignedInteger32(pk=True)
    name = Unicode(150, min_len=4, pattern='[a-z0-9.]+')
    family = Unicode(150)
    national_code = Unicode(10)
    father_name = Unicode(150)
    certificate_number = Unicode(10)
    birthday = Unicode(15)
    address = Unicode(250)
    # services = Array(ServiceModel).store_as('table')
    services = Iterable(ServiceModel)

    def __init__(self, uid, name, family, national_code, father_name, certificate_number, birthday, address, services):
        self.uid = uid
        self.name = name
        self.family = family
        self.national_code = national_code
        self.father_name = father_name
        self.certificate_number = certificate_number
        self.birthday = birthday
        self.address = address
        self.services = services
