from app.core_validators import (
    BirthdayCheckAdultValidator,
    BirthdayFormatValidator,
    CustomerExistsValidator,
    CustomerServiceLimitValidator,
    NationalCodeValidator,
)


class CustomerCreateValidation:
    def __init__(self):
        self.national_validator = NationalCodeValidator()
        self.birthday_format_validator = BirthdayFormatValidator()
        self.birthday_adult_validator = BirthdayCheckAdultValidator()

    def is_valid(self, payload):
        (self.national_validator.go_next(self.birthday_format_validator)
         .go_next(self.birthday_adult_validator))
        self.national_validator.validate(payload)


class ServiceCreateValidation:
    def __init__(self):
        self.customer_exist_validator = CustomerExistsValidator()
        self.service_validator = CustomerServiceLimitValidator()

    def is_valid(self, payload):
        self.customer_exist_validator.go_next(self.service_validator)
        self.customer_exist_validator.validate(payload)
