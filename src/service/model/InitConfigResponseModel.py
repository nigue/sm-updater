from dataclasses import dataclass


@dataclass(frozen=True)
class InitConfigResponseModel:
    texto: str