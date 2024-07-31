from dataclasses import dataclass


@dataclass(frozen=True)
class TraceLogRequestDTO:
    arcade_name: str
    log: str
    severity: str
