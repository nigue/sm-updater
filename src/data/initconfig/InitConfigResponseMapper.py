from abc import ABC

from src.data.Mapper import Mapper
from src.data.initconfig.dto.InitConfigResponseDTO import InitConfigResponseDTO
from src.service.model.InitConfigResponseModel import InitConfigResponseModel


class InitConfigResponseMapper(Mapper[InitConfigResponseDTO, InitConfigResponseModel], ABC):

    def map(self, dto: InitConfigResponseDTO) -> InitConfigResponseModel:
        for pack in dto.sm_pack:
            print(pack.id)
        return InitConfigResponseModel("")

