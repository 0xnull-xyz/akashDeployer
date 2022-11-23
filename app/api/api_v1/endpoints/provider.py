from fastapi import APIRouter, Body, Depends
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.security.jwt import allowed_create_base_resources
from app.crud.provider import create_provider, update_provider, get_providers_paginated
from app.crud.shortcuts import check_free_provider_title
from app.db.mongodb import get_database
from app.models.provider import EmbeddedProviderInDB, ProviderInResponse, ProviderInCreate, ProviderInUpdate
from app.models.shared import LimitOffsetPage, LimitOffsetParams

router = APIRouter()


@router.post("/provider", response_model=ProviderInResponse, tags=["providers"])
async def create_provider(
        provider: ProviderInCreate = Body(..., embed=True),
        db: AsyncIOMotorClient = Depends(get_database),
        dependencies=Depends(allowed_create_base_resources),
):
    await check_free_provider_title(db, provider.title)

    async with await db.start_session() as s:
        async with s.start_transaction():
            db_provider = await create_provider(db, provider)

            return ProviderInResponse(provider=db_provider)


@router.put("/provider", response_model=ProviderInResponse, tags=["providers"])
async def update_provider(
        provider: ProviderInUpdate = Body(..., embed=True),
        db: AsyncIOMotorClient = Depends(get_database),
        dependencies=Depends(allowed_create_base_resources),
):
    async with await db.start_session() as s:
        async with s.start_transaction():
            db_provider = await update_provider(db, provider.id, provider)

            return ProviderInResponse(provider=db_provider)


@router.get("/provider", response_model=LimitOffsetPage[EmbeddedProviderInDB], tags=["providers"])
async def get_providers(
        skip: int = 0, limit: int = 10,
        db: AsyncIOMotorClient = Depends(get_database),
):
    params = LimitOffsetParams(**{'offset': skip, 'limit': limit})
    async with await db.start_session() as db_apps:
        async with db_apps.start_transaction():
            db_apps = await get_providers_paginated(db, params)

            return db_apps
