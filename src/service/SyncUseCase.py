import os

from dotenv import load_dotenv

from src.data.initconfig.InitConfigResource import InitConfigResource
from src.data.initconfig.dto.InitConfigRequestModel import InitConfigRequestModel


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
        config = repository.process(model)
        print(f'End...')


