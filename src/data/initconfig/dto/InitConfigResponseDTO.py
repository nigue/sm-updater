from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class InitConfigResponseSmPackDTO:
    id: int
    identifier: str
    password: str
    destination: str
    internal: str
    file: str
    compress: bool
    sm_configuration_id: int


@dataclass(frozen=True)
class InitConfigResponseSmArcadePathsDTO:
    id: int
    stepmania_songs_path: str
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
