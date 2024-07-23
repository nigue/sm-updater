from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class InitConfigPackModel:
    md5: str
    file: str
    link: str
    folder: str
    compress: bool
    password: str
    final_name: str
    upload_date: str


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
