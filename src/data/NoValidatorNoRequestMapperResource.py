from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from src.data.ErrorHandler import ErrorHandler
from src.data.Mapper import Mapper
from src.data.Repository import Repository

B = TypeVar('B')
C = TypeVar('C')
D = TypeVar('D')


class NoValidatorNoRequestMapperResource(ABC, Generic[B, C, D]):
    def __init__(self,
                 repository: Repository[B, C],
                 error_handler: ErrorHandler[C],
                 response_mapper: Mapper[C, D]):
        self.repository = repository
        self.error_handler = error_handler
        self.response_mapper = response_mapper

    @abstractmethod
    def process(self, model: B) -> D:
        pass
