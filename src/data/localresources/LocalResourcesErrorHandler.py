from abc import ABC
from typing import List

from src.data.ErrorHandler import ErrorHandler
from src.data.initconfig.dto.InitConfigResponseDTO import InitConfigResponseSmPackDTO


class LocalResourcesErrorHandler(ErrorHandler[List[InitConfigResponseSmPackDTO]], ABC):
    def handle(self, dtos: List[InitConfigResponseSmPackDTO]) -> None:
        pass
