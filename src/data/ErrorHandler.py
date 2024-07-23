from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')


class ErrorHandler(ABC, Generic[T]):
    @abstractmethod
    def handle(self, model: T) -> None:
        pass