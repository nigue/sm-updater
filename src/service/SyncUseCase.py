import json
import os
import shutil
import zipfile
from dataclasses import asdict
from typing import List

import pixeldrain
import py7zr
from dotenv import load_dotenv

from src.data.initconfig.InitConfigResource import InitConfigResource
from src.data.initconfig.dto.InitConfigRequestModel import InitConfigRequestModel
from src.service.model.InitConfigResponseModel import InitConfigPackModel, InitConfigPathsModel


class SyncUseCase:

    @staticmethod
    def process():
        repository = InitConfigResource()
        load_dotenv()  # dotenv_path = Path('path/to/.env')
        model = InitConfigRequestModel(
            os.getenv("ARCADE_ID_NAME"),
            os.getenv("SUPABASE_USER_HASH"),
            os.getenv("SUPABASE_API_KEY")
        )
        # TODO try catch finnaly
        remote_conf = repository.process(model)
        div = "/"
        if remote_conf.so.lower().find("win") == 0:
            div = "\\"
        local_res = local_resources(remote_conf.paths.config)
        process_packs_list(remote_conf.packs, local_res, remote_conf.paths, div)
        print(f'Actualizando configuracion local')
        os.remove(remote_conf.paths.config)
        with open(remote_conf.paths.config, 'w', encoding='utf-8') as f:
            packs_dict = [asdict(pack) for pack in remote_conf.packs]
            json.dump(packs_dict, f, ensure_ascii=False, indent=4)
        print(f'End...')


def json_to_dataclass(dataclass_type, json_data):
    return dataclass_type(**json_data)


def local_resources(file: str) -> List[InitConfigPackModel]:
    result = []
    with open(file, 'r', encoding='utf-8') as json_data:
        contents = json.load(json_data)
    for item in contents:
        print(contents)
        result.append(json_to_dataclass(InitConfigPackModel, item))
    return result


def process_packs_list(
        remote: List[InitConfigPackModel],
        local: List[InitConfigPackModel],
        paths: InitConfigPathsModel,
        div: str
):
    if len(local) == 0:
        for remote_pack in remote:
            process_pack(remote_pack, paths, div)
    for remote_pack in remote:
        for local_pack in local:
            if remote_pack.equals(local_pack):
                print(f'Los archivos son iguales')
            else:
                print(f'Los archivos no son iguales')
                if remote_pack.final_name == local_pack.final_name:
                    file = f"{paths.sm}{div}{local_pack.folder}{div}{local_pack.final_name}"
                    os.remove(file)
                    print(f'Elimina pack local {file}')
                    process_pack(remote_pack, paths, div)


def process_pack(
        pack: InitConfigPackModel,
        paths: InitConfigPathsModel,
        div: str
):
    info = pixeldrain.info(pack.identifier)
    pixeldrain.download_file(
        pack.identifier,
        info['name'],
        f'{paths.downloads}{div}'
    )
    downloaded_file = f'{paths.downloads}{div}{info['name']}'
    print(f'Descarga pack {downloaded_file}')
    print(f'Prepara pack')
    print(f'Descomprime pack')
    with py7zr.SevenZipFile(
        f'{downloaded_file}',
            mode='r',
            password=pack.password) as initial_file:
        initial_file.extractall(path=f'{paths.downloads}{div}')
    print(f'Comprime pack')
    dir_compress = f'{paths.downloads}{div}{pack.internal}'
    file_to_compress = f'{paths.sm}{div}{pack.destination}{div}{pack.file}'
    store_zip_compression(dir_compress, file_to_compress)
    shutil.rmtree(dir_compress)
    os.remove(downloaded_file)


def store_zip_compression(dir_compress, file_to_compress):
    with zipfile.ZipFile(file_to_compress, 'w', zipfile.ZIP_STORED) as zipf:
        for root, dirs, files in os.walk(dir_compress):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, dir_compress))