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

    def equals(self, it) -> bool:
        result = True
        if not self.md5 == it.md5:
            result = False
        if not self.file == it.file:
            result = False
        if not self.link == it.link:
            result = False
        if not self.folder == it.folder:
            result = False
        if not self.compress == it.compress:
            result = False
        if not self.password == it.password:
            result = False
        if not self.final_name == it.final_name:
            result = False
        if not self.upload_date == it.upload_date:
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
