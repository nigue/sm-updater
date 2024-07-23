from abc import ABC

from src.data.ErrorHandler import ErrorHandler
from src.data.initconfig.dto.InitConfigResponseDTO import InitConfigResponseDTO
from src.excepcion.HandlerException import HandlerException


class InitConfigErrorHandler(ErrorHandler[InitConfigResponseDTO], ABC):
    def handle(self, dto: InitConfigResponseDTO) -> None:
        if not dto.id:
            e = "El valor id no puede estar vacío"
            print(f"Error: {e}")
            raise HandlerException(e)
