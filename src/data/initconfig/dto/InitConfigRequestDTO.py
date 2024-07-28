from dataclasses import dataclass


@dataclass(frozen=True)
class InitConfigRequestDTO:
    arcade_name: str
