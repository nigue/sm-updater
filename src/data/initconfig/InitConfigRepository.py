from abc import ABC
from supabase import create_client, Client

import os

from src.data.Repository import Repository
from src.data.initconfig.dto.InitConfigRequestDTO import InitConfigRequestDTO
from src.data.initconfig.dto.InitConfigResponseDTO import InitConfigResponseDTO


def json_to_dataclass(dataclass_type, json_data):
    return dataclass_type(**json_data)


class InitConfigRepository(Repository[InitConfigRequestDTO, InitConfigResponseDTO], ABC):

    def fetch(self, dto: InitConfigRequestDTO) -> InitConfigResponseDTO:
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")
        supabase: Client = create_client(url, key)
        response = (supabase.table("sm_configuration")
                    .select("*,sm_arcade_credentials(*),sm_arcade_paths(*),sm_pack(*)")
                    .eq("name", dto.arcade_name)
                    .limit(1)
                    .execute())
        return json_to_dataclass(InitConfigResponseDTO, response.data[0])

