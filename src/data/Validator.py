from abc import ABC, abstractmethod
from typing import TypeVar, Generic

# Definir un TypeVar para el tipo de entrada genérico
T = TypeVar('T')


class Validator(ABC, Generic[T]):
    @abstractmethod
    def validate(self, model: T) -> None:
        pass