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
                identifier=pack["identifier"],
                password=pack["password"],
                destination=pack["destination"],
                internal=pack["internal"],
                file=pack["file"],
                compress=pack["compress"],
                formal_name=pack["formal_name"]
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
                stepmania_songs_path=dto.sm_arcade_paths["stepmania_songs_path"],
                config=dto.sm_arcade_paths["config"],
                program=dto.sm_arcade_paths["program"],
                downloads=dto.sm_arcade_paths["downloads"]),
            packs=packs)


