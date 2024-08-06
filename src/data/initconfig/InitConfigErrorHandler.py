import os
from abc import ABC

from src.data.ErrorHandler import ErrorHandler
from src.data.initconfig.dto.InitConfigResponseDTO import InitConfigResponseDTO
from src.excepcion.HandlerException import HandlerException


class InitConfigErrorHandler(ErrorHandler[InitConfigResponseDTO], ABC):
    def handle(self, dto: InitConfigResponseDTO) -> None:
        for pack in dto.sm_pack:
            if not pack["identifier"]:
                e = "El valor identifier no puede estar vacío"
                print(f"Error: {e}")
                raise HandlerException(e)
            if not pack["password"]:
                e = "El valor password no puede estar vacío"
                print(f"Error: {e}")
                raise HandlerException(e)
            if not pack["destination"]:
                e = "El valor destination no puede estar vacío"
                print(f"Error: {e}")
                raise HandlerException(e)
            if not pack["internal"]:
                e = "El valor internal no puede estar vacío"
                print(f"Error: {e}")
                raise HandlerException(e)
            if not pack["file"]:
                e = "El valor file no puede estar vacío"
                print(f"Error: {e}")
                raise HandlerException(e)
            if not pack["compress"]:
                e = "El valor compress no puede estar vacío"
                print(f"Error: {e}")
                raise HandlerException(e)
        if not dto.realize:
            e = "El valor realize no puede estar vacío"
            print(f"Error: {e}")
            raise HandlerException(e)
        if not dto.so:
            e = "El valor so no puede estar vacío"
            print(f"Error: {e}")
            raise HandlerException(e)
        stepmania_songs = dto.sm_arcade_paths["stepmania_songs_path"]
        if not os.path.isdir(stepmania_songs):
            e = "Debe exsistir un directorio stepmania Songs"
            print(f"Error: {e}")
        if not os.access(stepmania_songs, os.R_OK):
            e = "Debe exsistir un directorio stepmania Songs, con persmisos de lectura"
            print(f"Error: {e}")
        if not os.access(stepmania_songs, os.W_OK):
            e = "Debe exsistir un directorio stepmania Songs, con persmisos de escritura"
            print(f"Error: {e}")
        if not os.path.isfile(dto.sm_arcade_paths["config"]):
            e = "Debe exsistir un archivo config"
            print(f"Error: {e}")
            raise HandlerException(e)
        if not os.path.isdir(dto.sm_arcade_paths["program"]):
            e = "Debe exsistir un directorio program"
            print(f"Error: {e}")
            raise HandlerException(e)
        if not os.path.isdir(dto.sm_arcade_paths["downloads"]):
            e = "Debe exsistir un directorio downloads"
            print(f"Error: {e}")
            raise HandlerException(e)
