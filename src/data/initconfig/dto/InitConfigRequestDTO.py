from dataclasses import dataclass


@dataclass(frozen=True)
class InitConfigRequestDTO:
    uri: str
    headers: dict[str, str]
