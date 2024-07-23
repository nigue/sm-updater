from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')


class Validator(ABC, Generic[T]):
    @abstractmethod
    def validate(self, model: T) -> None:
        pass
