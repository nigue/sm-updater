from dataclasses import dataclass


@dataclass(frozen=True)
class Persona:
    nombre: str
    edad: int
    direccion: str
