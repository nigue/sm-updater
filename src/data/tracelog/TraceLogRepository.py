import os
from abc import ABC

from supabase import create_client, Client

from src.data.Repository import Repository
from src.data.tracelog.TraceLogRequestDTO import TraceLogRequestDTO


class TraceLogRepository(Repository[TraceLogRequestDTO, None], ABC):

    def fetch(self, dto: TraceLogRequestDTO) -> None:
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")
        supabase: Client = create_client(url, key)
        (supabase.rpc("publish_report",
                      {
                          "configuration_name": dto.arcade_name,
                          "new_message": dto.log,
                          "new_severity": dto.severity,
                      })
         .execute())
