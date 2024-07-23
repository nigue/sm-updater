from abc import ABC, abstractmethod
from typing import TypeVar, Generic

# Definir los TypeVars para los tipos de entrada y salida genéricos
T = TypeVar('T')
U = TypeVar('U')


class Repository(ABC, Generic[T, U]):
    @abstractmethod
    def fetch(self, dto: T) -> U:
        pass