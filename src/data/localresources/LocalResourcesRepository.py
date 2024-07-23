from abc import ABC
from typing import List

import json

from src.data.Repository import Repository
from src.data.initconfig.dto.InitConfigResponseDTO import InitConfigResponseDTO, InitConfigResponseSmPackDTO


def json_to_dataclass(dataclass_type, json_data):
    return dataclass_type(**json_data)


class LocalResourcesRepository(Repository[str, List[InitConfigResponseSmPackDTO]], ABC):

    def fetch(self, file: str) -> List[InitConfigResponseSmPackDTO]:
        result = []
        json_data = json.load(open(file))
        for item in json_data:
            result.append(json_to_dataclass(InitConfigResponseDTO, item))
        return result

