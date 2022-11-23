from fastapi import APIRouter, Body, Depends
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.security.jwt import allowed_create_base_resources
from app.crud.dc import create_dc, update_dc, get_dcs_paginated
from app.crud.shortcuts import check_free_dc_title
from app.db.mongodb import get_database
from app.models.dc import EmbeddedDCInDB, DCInResponse, DCInCreate, DCInUpdate
from app.models.shared import LimitOffsetPage, LimitOffsetParams

router = APIRouter()


@router.post("/dc", response_model=DCInResponse, tags=["dcs"])
async def create_dc(
        dc: DCInCreate = Body(..., embed=True),
        db: AsyncIOMotorClient = Depends(get_database),
        dependencies=Depends(allowed_create_base_resources),
):
    await check_free_dc_title(db, dc.title)

    async with await db.start_session() as s:
        async with s.start_transaction():
            db_dc = await create_dc(db, dc)

            return DCInResponse(dc=db_dc)


@router.put("/dc", response_model=DCInResponse, tags=["dcs"])
async def update_dc(
        dc: DCInUpdate = Body(..., embed=True),
        db: AsyncIOMotorClient = Depends(get_database),
        dependencies=Depends(allowed_create_base_resources),
):
    async with await db.start_session() as s:
        async with s.start_transaction():
            db_dc = await update_dc(db, dc.id, dc)

            return DCInResponse(dc=db_dc)


@router.get("/dc", response_model=LimitOffsetPage[EmbeddedDCInDB], tags=["dcs"])
async def get_dcs(
        skip: int = 0, limit: int = 10,
        db: AsyncIOMotorClient = Depends(get_database),
):
    params = LimitOffsetParams(**{'offset': skip, 'limit': limit})
    async with await db.start_session() as db_apps:
        async with db_apps.start_transaction():
            db_apps = await get_dcs_paginated(db, params)

            return db_apps
