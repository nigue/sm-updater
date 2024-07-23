from abc import ABC
from typing import List

from src.data.NoValidatorNoRequestMapperResource import NoValidatorNoRequestMapperResource
from src.data.initconfig.dto.InitConfigResponseDTO import InitConfigResponseSmPackDTO
from src.data.localresources.LocalResourcesErrorHandler import LocalResourcesErrorHandler
from src.data.localresources.LocalResourcesRepository import LocalResourcesRepository
from src.data.localresources.LocalResourcesResponseMapper import LocalResourcesResponseMapper
from src.service.model.InitConfigResponseModel import InitConfigPackModel


class LocalResourcesResource(
    NoValidatorNoRequestMapperResource[
        str,
        List[InitConfigResponseSmPackDTO],
        List[InitConfigPackModel]],
    ABC
):

    def __init__(self):
        super().__init__(
            LocalResourcesRepository(),
            LocalResourcesErrorHandler(),
            LocalResourcesResponseMapper())

    def process(self, model: str) -> List[InitConfigPackModel]:
        response_dto = self.repository.fetch(model)
        self.error_handler.handle(response_dto)
        return self.response_mapper.map(response_dto)
