from abc import ABC

from src.data.Resource import Resource
from src.data.initconfig.InitConfigErrorHandler import InitConfigErrorHandler
from src.data.initconfig.InitConfigRepository import InitConfigRepository
from src.data.initconfig.InitConfigRequestMapper import InitConfigRequestMapper
from src.data.initconfig.InitConfigResponseMapper import InitConfigResponseMapper
from src.data.initconfig.InitConfigValidator import InitConfigValidator
from src.data.initconfig.dto.InitConfigRequestDTO import InitConfigRequestDTO
from src.data.initconfig.dto.InitConfigRequestModel import InitConfigRequestModel
from src.data.initconfig.dto.InitConfigResponseDTO import InitConfigResponseDTO
from src.service.model.InitConfigResponseModel import InitConfigResponseModel


class InitConfigResource(
    Resource[
        InitConfigRequestModel,
        InitConfigRequestDTO,
        InitConfigResponseDTO,
        InitConfigResponseModel],
    ABC
):

    def __init__(self):
        super().__init__(
            InitConfigValidator(),
            InitConfigRequestMapper(),
            InitConfigRepository(),
            InitConfigErrorHandler(),
            InitConfigResponseMapper())

    def process(self, model: InitConfigRequestModel) -> InitConfigResponseModel:
        self.validator.validate(model)
        request_dto = self.request_mapper.map(model)
        response_dto = self.repository.fetch(request_dto)
        self.error_handler.handle(response_dto)
        return self.response_mapper.map(response_dto)
