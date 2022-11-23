from typing import Optional

from pydantic import EmailStr
from starlette.exceptions import HTTPException
from starlette.status import (
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from .dc import get_dc
from .deployment import get_deployment
from .deployment_type import get_deployment_type
from .provider import get_provider
from .region import get_region
from .sdl_template import get_sdl_template
from .tag import get_tag
from .user import get_user, get_user_by_email
from ..db.mongodb import AsyncIOMotorClient


async def check_free_username_and_email(
        conn: AsyncIOMotorClient, username: Optional[str] = None, email: Optional[EmailStr] = None
):
    if username:
        user_by_username = await get_user(conn, username)
        if user_by_username:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="User with this username already exists",
            )
    if email:
        user_by_email = await get_user_by_email(conn, email)
        if user_by_email:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="User with this email already exists",
            )


async def check_free_tag_title(
        conn: AsyncIOMotorClient, title: Optional[str] = None
):
    if title:
        tag_by_title = await get_tag(conn, title)
        if tag_by_title:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Tag with this title already exists",
            )
    else:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Tag must have title",
        )


async def check_free_sdl_template_title(
        conn: AsyncIOMotorClient, title: Optional[str] = None
):
    if title:
        sdl_tmp_by_title = await get_sdl_template(conn, title)
        if sdl_tmp_by_title:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="SDL Template with this title already exists",
            )
    else:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail="SDL Template must have title",
        )


async def check_free_provider_title(
        conn: AsyncIOMotorClient, title: Optional[str] = None
):
    if title:
        provider_by_title = await get_provider(conn, title)
        if provider_by_title:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Provider with this title already exists",
            )
    else:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Provider must have title",
        )


async def check_free_region_title(
        conn: AsyncIOMotorClient, title: Optional[str] = None
):
    if title:
        region_by_title = await get_region(conn, title)
        if region_by_title:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Region with this title already exists",
            )
    else:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Region must have title",
        )


async def check_free_deployment_type_title(
        conn: AsyncIOMotorClient, title: Optional[str] = None
):
    if title:
        deployment_type_by_title = await get_deployment_type(conn, title)
        if deployment_type_by_title:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Deployment Type with this title already exists",
            )
    else:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Deployment Type must have title",
        )


async def check_free_deployment_title(
        conn: AsyncIOMotorClient, title: Optional[str] = None
):
    if title:
        deployment_by_title = await get_deployment(conn, title)
        if deployment_by_title:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Deployment with this title already exists",
            )
    else:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Deployment must have title",
        )


async def check_free_dc_title(
        conn: AsyncIOMotorClient, title: Optional[str] = None
):
    if title:
        dc_by_title = await get_dc(conn, title)
        if dc_by_title:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="DC with this title already exists",
            )
    else:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail="DC must have title",
        )
