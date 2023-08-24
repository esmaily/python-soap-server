from abc import ABC, abstractmethod
from typing import Any, Optional


class Singleton(type):
    """
     The Singleton class can be implemented in f Python
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


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


class Orm(ABC):

    @abstractmethod
    def get_all(self, order_by: str):
        pass

    @abstractmethod
    def get_by_id(self, model_id: int):
        pass

    @abstractmethod
    def get_by(self, **kwargs):
        pass

    @abstractmethod
    def store(self, data: dict):
        pass

    @abstractmethod
    def update(self, model_id: int, data: dict):
        pass

    @abstractmethod
    def destroy(self, model_id: int):
        pass


class Context():

    def __init__(self, orm: Orm) -> None:
        self._orm = orm

    @property
    def orm(self) -> Orm:
        return self._orm

    @orm.setter
    def orm(self, orm: Orm) -> None:
        self._orm = orm
