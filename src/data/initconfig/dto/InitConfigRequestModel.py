from dataclasses import dataclass


@dataclass(frozen=True)
class InitConfigRequestModel:
    arcade: str
    user: str
    key: str
