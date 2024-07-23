from abc import ABC, abstractmethod
from typing import TypeVar, Generic

# Definir los TypeVars para los tipos de entrada y salida genéricos
T1 = TypeVar('T1')
T2 = TypeVar('T2')
R = TypeVar('R')


class BiMapper(ABC, Generic[T1, T2, R]):
    @abstractmethod
    def map(self, model: T1, dto: T2) -> R:
        pass