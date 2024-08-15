import os
from abc import ABC

from supabase import create_client, Client

from src.conf.Prop import Prop
from src.data.Repository import Repository
from src.data.tracelog.TraceLogRequestDTO import TraceLogRequestDTO


class CleanProgramRepository(Repository[str, None], ABC):

    def fetch(self, arcade_name: str) -> None:
        url: str = Prop.SUPABASE_URL
        key: str = Prop.SUPABASE_KEY
        supabase: Client = create_client(url, key)
        (supabase.rpc("update_program",
                      {
                          "configuration_name": arcade_name,
                          "program_identifier": '',
                      })
         .execute())
