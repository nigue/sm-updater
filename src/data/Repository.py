from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')
U = TypeVar('U')


class Repository(ABC, Generic[T, U]):
    @abstractmethod
    def fetch(self, dto: T) -> U:
        pass
