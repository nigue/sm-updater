import os
from typing import List

from dotenv import load_dotenv

from src.data.initconfig.InitConfigResource import InitConfigResource
from src.data.initconfig.dto.InitConfigRequestModel import InitConfigRequestModel
from src.data.localresources.LocalResourcesResource import LocalResourcesResource
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
        #TODO try catch finnaly
        remote_conf = repository.process(model)
        local_res = LocalResourcesResource().process(remote_conf.paths.config)
        process_packs_list(remote_conf.packs, local_res, remote_conf.paths)
        print(f'End...')


def process_packs_list(
        remote: List[InitConfigPackModel],
        local: List[InitConfigPackModel],
        paths: InitConfigPathsModel
):
    if len(local) == 0:
        for remote_pack in remote:
            process_pack(remote_pack, paths)
    for remote_pack in remote:
        for local_pack in local:
            if remote_pack.equals(local_pack):
                print(f'Los archivos son iguales')
            else:
                print(f'Los archivos no son iguales')
                if remote_pack.final_name == local_pack.final_name:
                    print(f'Elimina pack local')
                    process_pack(remote_pack, paths)


def process_pack(
        remote: InitConfigPackModel,
        paths: InitConfigPathsModel
):
    print(f'Descarga pack')
    print(f'Prepara pack')
    pass