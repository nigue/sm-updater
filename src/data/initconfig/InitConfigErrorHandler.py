import os
from abc import ABC

from src.data.ErrorHandler import ErrorHandler
from src.data.initconfig.dto.InitConfigResponseDTO import InitConfigResponseDTO
from src.excepcion.HandlerException import HandlerException


class InitConfigErrorHandler(ErrorHandler[InitConfigResponseDTO], ABC):
    def handle(self, dto: InitConfigResponseDTO) -> None:
        for pack in dto.sm_pack:
            if not pack["md5"]:
                e = "El valor md5 no puede estar vacío"
                print(f"Error: {e}")
            if not pack["file"]:
                e = "El valor file no puede estar vacío"
                print(f"Error: {e}")
            if not pack["link"]:
                e = "El valor link no puede estar vacío"
                print(f"Error: {e}")
            if not pack["folder"]:
                e = "El valor folder no puede estar vacío"
                print(f"Error: {e}")
            if not pack["compress"]:
                e = "El valor compress no puede estar vacío"
                print(f"Error: {e}")
            if not pack["password"]:
                e = "El valor password no puede estar vacío"
                print(f"Error: {e}")
            if not pack["final_name"]:
                e = "El valor final_name no puede estar vacío"
                print(f"Error: {e}")
            if not pack["upload_date"]:
                e = "El valor upload_date no puede estar vacío"
                print(f"Error: {e}")
        if not dto.realize:
            e = "El valor realize no puede estar vacío"
            print(f"Error: {e}")
            raise HandlerException(e)
        if not dto.so:
            e = "El valor so no puede estar vacío"
            print(f"Error: {e}")
            raise HandlerException(e)
        if not os.path.isdir(dto.sm_arcade_paths["sm"]):
            e = "Debe exsistir un directorio sm"
            print(f"Error: {e}")
            raise HandlerException(e)
        div = "/"
        if dto.so.lower().find("win") == 0:
            div = "\\"
        if not os.path.isdir(f'{dto.sm_arcade_paths["sm"]}{div}Characters'):
            e = "Debe exsistir un directorio sm Characters"
            print(f"Error: {e}")
            raise HandlerException(e)
        if not os.path.isdir(f'{dto.sm_arcade_paths["sm"]}{div}NoteSkins'):
            e = "Debe exsistir un directorio sm NoteSkins"
            print(f"Error: {e}")
            raise HandlerException(e)
        if not os.path.isdir(f'{dto.sm_arcade_paths["sm"]}{div}Packages'):
            e = "Debe exsistir un directorio sm Packages"
            print(f"Error: {e}")
            raise HandlerException(e)
        if not os.path.isdir(f'{dto.sm_arcade_paths["sm"]}{div}Themes'):
            e = "Debe exsistir un directorio sm Themes"
            print(f"Error: {e}")
            raise HandlerException(e)
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
