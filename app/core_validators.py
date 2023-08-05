from abc import ABC, abstractmethod
from datetime import date, timedelta
from typing import Any, Optional

from spyne.error import ValidationError


class Validator(ABC):
    """Parent class of all concrete validator"""

    @abstractmethod
    def go_next(self, validator):
        pass

    @abstractmethod
    def validate(self, request) -> Optional[str]:
        pass


class AbstractValidator(Validator):
    """
    The default chaining behavior  for validations
    class.
    """

    _go_validator: Validator = None

    def go_next(self, validator: Validator) -> Validator:
        self._go_validator = validator
        return validator

    @abstractmethod
    def validate(self, request: Any) -> str:
        if self._go_validator:
            return self._go_validator.validate(request)

        return None


class NationalCodeValidator(AbstractValidator):

    def validate(self, request: Any) -> str:
        if len(request["national_code"]) != 10:
            raise ValidationError("national code must be 10 length")
        else:
            return super().validate(request)


class BirthdayFormatValidator(AbstractValidator):

    def validate(self, request: Any) -> str:
        try:
            date.fromisoformat(request["birthday"])
        except ValueError:
            raise ValidationError("Incorrect birthday format, should be YYYY-MM-DD")

        return super().validate(request)


class BirthdayCheckAdultValidator(AbstractValidator):

    def validate(self, request: Any) -> str:
        today = date.today()
        birth = date.fromisoformat(request["birthday"])
        age = (today - birth) // timedelta(days=365.2425)
        if age < 18:
            raise ValidationError("your birthday must be greater than 18")
        else:
            return super().validate(request)


class CustomerExistsValidator(AbstractValidator):

    def validate(self, request: Any) -> str:
        if not request["customer"]:
            raise ValidationError("customer not exists")
        else:
            return super().validate(request)


class CustomerServiceLimitValidator(AbstractValidator):

    def validate(self, request: Any) -> str:
        if len(request["services"]) >= 10:
            raise ValidationError("every customer can create 10 services")
        else:
            return super().validate(request)
