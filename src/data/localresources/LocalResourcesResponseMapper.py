from abc import ABC
from typing import List

from src.data.Mapper import Mapper
from src.data.initconfig.dto.InitConfigResponseDTO import InitConfigResponseSmPackDTO
from src.service.model.InitConfigResponseModel import InitConfigPackModel


class LocalResourcesResponseMapper(Mapper[List[InitConfigResponseSmPackDTO], List[InitConfigPackModel]], ABC):

    def map(self, dtos: List[InitConfigResponseSmPackDTO]) -> List[InitConfigPackModel]:
        packs = []
        for pack in dtos:
            packs.append(InitConfigPackModel(
                md5=pack["md5"],
                file=pack["file"],
                link=pack["link"],
                folder=pack["folder"],
                compress=pack["compress"],
                password=pack["password"],
                final_name=pack["final_name"],
                upload_date=pack["upload_date"]
            ))
        return packs
