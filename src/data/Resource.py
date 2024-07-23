from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from src.data.ErrorHandler import ErrorHandler
from src.data.Mapper import Mapper
from src.data.Repository import Repository
from src.data.Validator import Validator

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')
D = TypeVar('D')


class Resource(ABC, Generic[A, B, C, D]):
    def __init__(self,
                 validator: Validator[A],
                 request_mapper: Mapper[A, B],
                 repository: Repository[B, C],
                 error_handler: ErrorHandler[C],
                 response_mapper: Mapper[C, D]):
        self.validator = validator
        self.request_mapper = request_mapper
        self.repository = repository
        self.error_handler = error_handler
        self.response_mapper = response_mapper

    @abstractmethod
    def process(self, model: A) -> D:
        pass
