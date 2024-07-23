from abc import ABC

import requests

from src.data.Repository import Repository
from src.data.initconfig.dto.InitConfigRequestDTO import InitConfigRequestDTO
from src.data.initconfig.dto.InitConfigResponseDTO import InitConfigResponseDTO
from src.excepcion.RestException import RestException


def json_to_dataclass(dataclass_type, json_data):
    return dataclass_type(**json_data)


class InitConfigRepository(Repository[InitConfigRequestDTO, InitConfigResponseDTO], ABC):

    def fetch(self, dto: InitConfigRequestDTO) -> InitConfigResponseDTO:
        try:
            response = requests.get(dto.uri, headers=dto.headers)
            response.raise_for_status()
            return json_to_dataclass(InitConfigResponseDTO, response.json()[0])
        except requests.exceptions.HTTPError as errh:
            print("HTTP Error:", errh)
            raise RestException(errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error de Conexión:", errc)
            raise RestException(errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
            raise RestException(errt)
        except requests.exceptions.RequestException as err:
            print("Error:", err)
            raise RestException(err)

