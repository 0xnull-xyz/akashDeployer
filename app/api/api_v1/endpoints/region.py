from fastapi import APIRouter, Body, Depends
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.security.jwt import allowed_create_base_resources
from app.crud.region import create_region, update_region, get_regions_paginated
from app.crud.shortcuts import check_free_region_title
from app.db.mongodb import get_database
from app.models.region import EmbeddedRegionInDB, RegionInResponse, RegionInCreate, RegionInUpdate
from app.models.shared import LimitOffsetPage, LimitOffsetParams

router = APIRouter()


@router.post("/region", response_model=RegionInResponse, tags=["regions"])
async def create_region(
        region: RegionInCreate = Body(..., embed=True),
        db: AsyncIOMotorClient = Depends(get_database),
        dependencies=Depends(allowed_create_base_resources),
):
    await check_free_region_title(db, region.title)

    async with await db.start_session() as s:
        async with s.start_transaction():
            db_region = await create_region(db, region)

            return RegionInResponse(region=db_region)


@router.put("/region", response_model=RegionInResponse, tags=["regions"])
async def update_region(
        region: RegionInUpdate = Body(..., embed=True),
        db: AsyncIOMotorClient = Depends(get_database),
        dependencies=Depends(allowed_create_base_resources),
):
    async with await db.start_session() as s:
        async with s.start_transaction():
            db_region = await update_region(db, region.id, region)

            return RegionInResponse(region=db_region)


@router.get("/region", response_model=LimitOffsetPage[EmbeddedRegionInDB], tags=["regions"])
async def get_regions(
        skip: int = 0, limit: int = 10,
        db: AsyncIOMotorClient = Depends(get_database),
):
    params = LimitOffsetParams(**{'offset': skip, 'limit': limit})
    async with await db.start_session() as db_apps:
        async with db_apps.start_transaction():
            db_apps = await get_regions_paginated(db, params)

            return db_apps
