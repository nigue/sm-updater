from abc import ABC

from src.data.Mapper import Mapper
from src.data.initconfig.dto.InitConfigResponseDTO import InitConfigResponseDTO
from src.service.model.InitConfigResponseModel import InitConfigResponseModel, InitConfigPackModel, \
    InitConfigCredentialsModel, InitConfigPathsModel


class InitConfigResponseMapper(Mapper[InitConfigResponseDTO, InitConfigResponseModel], ABC):

    def map(self, dto: InitConfigResponseDTO) -> InitConfigResponseModel:
        packs = []
        for pack in dto.sm_pack:
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
        return InitConfigResponseModel(
            name=dto.name,
            realize=dto.realize,
            so=dto.so,
            sm=dto.sm,
            credentials=InitConfigCredentialsModel(
                pixeldrain_key=dto.sm_arcade_credentials["pixeldrain_key"],
                pixeldrain_secret=dto.sm_arcade_credentials["pixeldrain_secret"]),
            paths=InitConfigPathsModel(
                sm=dto.sm_arcade_paths["sm"],
                config=dto.sm_arcade_paths["config"],
                program=dto.sm_arcade_paths["program"],
                downloads=dto.sm_arcade_paths["downloads"]),
            packs=packs)


