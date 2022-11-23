from fastapi import APIRouter, Body, Depends
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.security.jwt import allowed_create_base_resources, allowed_access_base_resources, \
    get_current_user_authorizer
from app.crud.shortcuts import check_free_tag_title
from app.crud.tag import create_tag, update_tag, get_tags_paginated
from app.db.mongodb import get_database
from app.models.shared import LimitOffsetPage, LimitOffsetParams
from app.models.tag import EmbeddedTagInDB, TagInResponse, TagInCreate, TagInUpdate
from app.models.user import User

router = APIRouter()


@router.post("/tag", response_model=TagInResponse, tags=["tags"])
async def create_tag(
        tag: TagInCreate = Body(..., embed=True),
        db: AsyncIOMotorClient = Depends(get_database),
        dependencies=Depends(allowed_create_base_resources),
):
    await check_free_tag_title(db, tag.title)

    async with await db.start_session() as s:
        async with s.start_transaction():
            db_tag = await create_tag(db, tag)

            return TagInResponse(tag=db_tag)


@router.put("/tag", response_model=TagInResponse, tags=["tags"])
async def update_tag(
        tag: TagInUpdate = Body(..., embed=True),
        db: AsyncIOMotorClient = Depends(get_database),
        dependencies=Depends(allowed_create_base_resources),
):
    async with await db.start_session() as s:
        async with s.start_transaction():
            db_tag = await update_tag(db, tag.id, tag)

            return TagInResponse(tag=db_tag)


@router.get("/tag", response_model=LimitOffsetPage[EmbeddedTagInDB], tags=["tags"])
async def get_tags(
        skip: int = 0, limit: int = 10,
        db: AsyncIOMotorClient = Depends(get_database),
        dependencies=Depends(allowed_access_base_resources),
):
    params = LimitOffsetParams(**{'offset': skip, 'limit': limit})
    async with await db.start_session() as db_apps:
        async with db_apps.start_transaction():
            db_apps = await get_tags_paginated(db, params)

            return db_apps


@router.get("/tag/my", response_model=LimitOffsetPage[EmbeddedTagInDB], tags=["tags"])
async def get_my_tags(
        skip: int = 0, limit: int = 10,
        db: AsyncIOMotorClient = Depends(get_database),
        user: User = Depends(get_current_user_authorizer(required=True)),
):
    params = LimitOffsetParams(**{'offset': skip, 'limit': limit})
    async with await db.start_session() as db_apps:
        async with db_apps.start_transaction():
            db_apps = await get_tags_paginated(db, params, user.id)

            return db_apps
