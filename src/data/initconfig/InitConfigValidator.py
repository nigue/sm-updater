from abc import ABC

from src.data.Validator import Validator
from src.data.initconfig.dto.InitConfigRequestModel import InitConfigRequestModel


class InitConfigValidator(Validator[InitConfigRequestModel], ABC):
    def validate(self, model: InitConfigRequestModel) -> None:
        if not model.arcade:
            e = "El valor arcade no puede estar vacío"
            print(f"Error: {e}")
            raise ValueError(e)