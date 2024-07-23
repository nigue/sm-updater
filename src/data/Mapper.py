from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')
U = TypeVar('U')


class Mapper(ABC, Generic[T, U]):
    @abstractmethod
    def map(self, model: T) -> U:
        pass