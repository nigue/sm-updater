from dataclasses import dataclass
from enum import Enum


class LogLevel(Enum):
    Error = "Error"
    Info = "Info"


@dataclass(frozen=True)
class TraceLogRequestDTO:
    arcade_name: str
    log: str
    severity: LogLevel
