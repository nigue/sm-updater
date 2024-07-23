from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class InitConfigResponseSmPackDTO:
    id: int
    md5: str
    file: str
    link: str
    folder: str
    compress: bool
    password: str
    final_name: str
    upload_date: str
    sm_configuration_id: int


@dataclass(frozen=True)
class InitConfigResponseSmArcadePathsDTO:
    id: int
    sm: str
    config: str
    program: str
    downloads: str


@dataclass(frozen=True)
class InitConfigResponseSmArcadeCredentialsDTO:
    id: int
    pixeldrain_key: str
    pixeldrain_secret: str


@dataclass(frozen=True)
class InitConfigResponseDTO:
    id: int
    name: str
    realize: int
    so: str
    sm: str
    fk_credentials: int
    fk_paths: int
    sm_arcade_credentials: InitConfigResponseSmArcadeCredentialsDTO
    sm_arcade_paths: InitConfigResponseSmArcadePathsDTO
    sm_pack: List[InitConfigResponseSmPackDTO]
