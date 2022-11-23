from fastapi import APIRouter, Body, Depends
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.security.jwt import allowed_create_base_resources
from app.crud.sdl_template import create_sdl_template, update_sdl_template, get_sdl_templates_paginated
from app.crud.shortcuts import check_free_sdl_template_title
from app.db.mongodb import get_database
from app.models.sdl_template import EmbeddedSDLTemplateInDB, SDLTemplateInResponse, SDLTemplateInCreate, \
    SDLTemplateInUpdate
from app.models.shared import LimitOffsetPage, LimitOffsetParams

router = APIRouter()


@router.post("/sdl_template", response_model=SDLTemplateInResponse, tags=["sdl_templates"])
async def create_sdl_template(
        sdl_template: SDLTemplateInCreate = Body(..., embed=True),
        db: AsyncIOMotorClient = Depends(get_database),
        dependencies=Depends(allowed_create_base_resources),
):
    await check_free_sdl_template_title(db, sdl_template.title)

    async with await db.start_session() as s:
        async with s.start_transaction():
            db_sdl_template = await create_sdl_template(db, sdl_template)

            return SDLTemplateInResponse(sdl_template=db_sdl_template)


@router.put("/sdl_template", response_model=SDLTemplateInResponse, tags=["sdl_templates"])
async def update_sdl_template(
        sdl_template: SDLTemplateInUpdate = Body(..., embed=True),
        db: AsyncIOMotorClient = Depends(get_database),
        dependencies=Depends(allowed_create_base_resources),
):
    async with await db.start_session() as s:
        async with s.start_transaction():
            db_sdl_template = await update_sdl_template(db, sdl_template.id, sdl_template)

            return SDLTemplateInResponse(sdl_template=db_sdl_template)


@router.get("/sdl_template", response_model=LimitOffsetPage[EmbeddedSDLTemplateInDB], tags=["sdl_templates"])
async def get_sdl_templates(
        skip: int = 0, limit: int = 10,
        db: AsyncIOMotorClient = Depends(get_database),
):
    params = LimitOffsetParams(**{'offset': skip, 'limit': limit})
    async with await db.start_session() as db_apps:
        async with db_apps.start_transaction():
            db_apps = await get_sdl_templates_paginated(db, params)

            return db_apps
