# from spyne import Unicode
from spyne.model.complex import ComplexModelBase, ComplexModelMeta, Array
from spyne.model.primitive import UnsignedInteger32, Unicode
from sqlalchemy import MetaData
import sqlalchemy


class TableModel(ComplexModelBase):
    __metaclass__ = ComplexModelMeta
    __metadata__ = MetaData()


class Service(TableModel):
    __tablename__ = 'service'
    __namespace__ = 'spyne.examples.customer_manager'
    __table_args__ = {"sqlite_autoincrement": True}
    id = UnsignedInteger32(pk=True)
    name = Unicode(150)
    number = Unicode(200)


class Customer(TableModel):
    __tablename__ = 'customer'
    __namespace__ = 'spyne.examples.customer_manager'
    __table_args__ = {"sqlite_autoincrement": True}

    # mapper_registry.metadata
    id = UnsignedInteger32(pk=True)
    first_name = Unicode(150, min_len=4, pattern='[a-z0-9.]+')
    last_name = Unicode(150)
    national_code = Unicode(10)
    father_name = Unicode(150)
    certificate_number = Unicode(10)
    birthday = Unicode(15)
    address = Unicode(250)
    # services = Array(Service).store_as('table')
