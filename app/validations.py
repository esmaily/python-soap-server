from app.core_validators import BirthdayFormatValidator, BirthdayCheckAdultValidator, NationalCodeValidator, \
    ServiceLimitValidator


class CustomerValidation:
    def __init__(self):
        self.national_validator = NationalCodeValidator()
        self.birthday_format_validator = BirthdayFormatValidator()
        self.birthday_adult_validator = BirthdayCheckAdultValidator()
        self.service_limit_validator = ServiceLimitValidator()

    def is_valid(self, payload):
        (self.national_validator.go_next(self.birthday_format_validator)
         .go_next(self.birthday_adult_validator).go_next(self.service_limit_validator))
        self.national_validator.validate(payload)
