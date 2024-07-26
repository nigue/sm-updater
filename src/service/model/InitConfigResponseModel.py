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


@dataclass(frozen=True)
class InitConfigPathsModel:
    stepmania: str
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
