from abc import ABC

from src.data.Mapper import Mapper
from src.data.initconfig.dto.InitConfigRequestDTO import InitConfigRequestDTO
from src.data.initconfig.dto.InitConfigRequestModel import InitConfigRequestModel


class InitConfigRequestMapper(Mapper[InitConfigRequestModel, InitConfigRequestDTO], ABC):

    def map(self, model: InitConfigRequestModel) -> InitConfigRequestDTO:
        return InitConfigRequestDTO(model.arcade)
