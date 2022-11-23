import platform

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from starlette.responses import JSONResponse


def create_aliased_response(model: BaseModel) -> JSONResponse:
    return JSONResponse(content=jsonable_encoder(model, by_alias=True))


def which_os() -> str:
    return platform.system()


def is_mac() -> bool:
    return which_os().lower() == 'darwin'
