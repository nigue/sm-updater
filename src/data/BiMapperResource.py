from abc import ABC, abstractmethod
from typing import TypeVar

from src.data.BiMapper import BiMapper
from src.data.ErrorHandler import ErrorHandler
from src.data.Mapper import Mapper
from src.data.Repository import Repository
from src.data.Validator import Validator

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')
D = TypeVar('D')


class BiMapperResource(ABC):
    def __init__(self,
                 validator: Validator[A],
                 request_mapper: Mapper[A, B],
                 repository: Repository[B, C],
                 error_handler: ErrorHandler[C],
                 response_mapper: BiMapper[A, C, D]):
        self.validator = validator
        self.request_mapper = request_mapper
        self.repository = repository
        self.error_handler = error_handler
        self.response_mapper = response_mapper

    @abstractmethod
    def process(self, model: A) -> D:
        self.validator.validate(model)
        request_dto = self.request_mapper.map(model)
        response_dto = self.repository.fetch(request_dto)
        self.error_handler.handle(response_dto)
        return self.response_mapper.map(model, response_dto)
