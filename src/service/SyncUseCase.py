import json
import os
import shutil
import zipfile
from dataclasses import asdict
from typing import List

import pixeldrain
import py7zr

from src.conf.Prop import Prop
from src.data.initconfig.InitConfigResource import InitConfigResource
from src.data.initconfig.dto.InitConfigRequestModel import InitConfigRequestModel
from src.data.tracelog.TraceLogRepository import TraceLogRepository
from src.data.tracelog.TraceLogRequestDTO import TraceLogRequestDTO
from src.service.model.InitConfigResponseModel import InitConfigPackModel, InitConfigPathsModel


class SyncUseCase:

    @staticmethod
    def process():
        repository = InitConfigResource()
        model = InitConfigRequestModel(Prop.ARCADE_ID_NAME)
        trace = TraceLogRepository()
        try:
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
            trace.fetch(TraceLogRequestDTO(model.arcade, f"Packs procesados {len(remote_conf.packs)}", 'Info'))
        except Exception as error:
            trace.fetch(TraceLogRequestDTO(model.arcade, str(error), 'Error'))


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
    for remote_pack in remote:
        procesable = True
        for local_pack in local:
            if remote_pack.file == local_pack.file:
                print(f'Mismo pack {remote_pack.file}')
                if not remote_pack.identifier == local_pack.identifier:
                    print(f'Update pack {remote_pack.file}')
                    pack_dir = f"{paths.stepmania_songs_path}{div}{local_pack.formal_name}"
                    shutil.rmtree(pack_dir)
                    print(f'Elimina pack local {pack_dir}')
                else:
                    procesable = False
            else:
                print(f'Nuevo pack {remote_pack.file}')
        if procesable:
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
    temporal_dir = f'{paths.downloads}{div}temporal'
    os.mkdir(temporal_dir)
    with py7zr.SevenZipFile(
            downloaded_file,
            mode='r',
            password=pack.password) as initial_file:
        initial_file.extractall(path=temporal_dir)
    #todo ya no comprime, ahora debe mover
    print(f'Mover pack')
    dir_to_move = f'{temporal_dir}{div}Songs{div}{pack.formal_name}'
    dist_to_move = f'{paths.stepmania_songs_path}{div}{pack.formal_name}'
    shutil.copytree(dir_to_move, dist_to_move)
    shutil.rmtree(temporal_dir)
    os.remove(downloaded_file)


def store_zip_compression(dir_compress, file_to_compress):
    with zipfile.ZipFile(file_to_compress, 'w', zipfile.ZIP_STORED) as zipf:
        for root, dirs, files in os.walk(dir_compress):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, dir_compress))