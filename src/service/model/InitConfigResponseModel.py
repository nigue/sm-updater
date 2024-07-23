from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class InitConfigPackModel:
    identifier: str
    password: str
    destination: str
    internal: str
    file: str
    compress: bool

    def equals(self, it) -> bool:
        result = True
        if not self.identifier == it.identifier:
            result = False
        if not self.password == it.password:
            result = False
        if not self.destination == it.destination:
            result = False
        if not self.internal == it.internal:
            result = False
        if not self.file == it.file:
            result = False
        if not self.compress == it.compress:
            result = False
        return result


@dataclass(frozen=True)
class InitConfigPathsModel:
    sm: str
    config: str
    program: str
    downloads: str


@dataclass(frozen=True)
class InitConfigCredentialsModel:
    pixeldrain_key: str
    pixeldrain_secret: str


@dataclass(frozen=True)
class InitConfigResponseModel:
    name: str
    realize: int
    so: str
    sm: str
    credentials: InitConfigCredentialsModel
    paths: InitConfigPathsModel
    packs: List[InitConfigPackModel]
