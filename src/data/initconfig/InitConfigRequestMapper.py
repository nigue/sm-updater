from abc import ABC

from src.data.Mapper import Mapper
from src.data.initconfig.dto.InitConfigRequestDTO import InitConfigRequestDTO
from src.data.initconfig.dto.InitConfigRequestModel import InitConfigRequestModel


class InitConfigRequestMapper(Mapper[InitConfigRequestModel, InitConfigRequestDTO], ABC):

    def map(self, model: InitConfigRequestModel) -> InitConfigRequestDTO:
        uri = f"https://{model.user}.supabase.co/rest/v1/sm_configuration?"
        uri += f"name=eq.{model.arcade}&"
        uri += "select=*,sm_arcade_credentials(*),sm_arcade_paths(*),sm_pack(*)&"
        uri += "limit=1"
        headers = {
            'Authorization': f"Bearer {model.key}",
            'apikey': model.key
        }
        return InitConfigRequestDTO(uri, headers)
