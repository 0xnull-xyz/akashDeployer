import datetime
from typing import Optional

from bson.objectid import ObjectId
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from app.core.configs.config import database_name, providers_collection_name
from app.db.mongodb import AsyncIOMotorClient
from app.models.provider import ProviderInCreate, ProviderInDB, ProviderInUpdate, EmbeddedProviderInDB, ProvidersInDB
from app.models.shared import LimitOffsetParams, LimitOffsetPage


async def get_provider(conn: AsyncIOMotorClient, title: str) -> Optional[ProviderInDB]:
    row = await conn[database_name][providers_collection_name].find_one({"title": title})
    if row:
        return ProviderInDB(**row)


# noinspection PyShadowingBuiltins
async def get_provider_by_id(conn: AsyncIOMotorClient, id: str) -> Optional[ProviderInDB]:
    try:
        row = await conn[database_name][providers_collection_name].find_one({"_id": ObjectId(id)})
        if row:
            return ProviderInDB(**row)
    except Exception as e:
        # @254: log
        return None


async def create_provider(conn: AsyncIOMotorClient, provider: ProviderInCreate) -> ProviderInDB:
    db_provider = ProviderInDB(**provider.dict())

    row = await conn[database_name][providers_collection_name].insert_one(db_provider.dict())

    db_provider.id = row.inserted_id

    return db_provider


async def update_provider(conn: AsyncIOMotorClient, id: str, provider: ProviderInUpdate) -> ProviderInDB:
    db_provider = await get_provider_by_id(conn, id)
    if not db_provider:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Incorrect provider id"
        )

    db_provider.title = provider.title or db_provider.title
    db_provider.desc = provider.desc or db_provider.desc
    db_provider.updated_at = datetime.datetime.utcnow()

    updated_at = await conn[database_name][providers_collection_name] \
        .update_one({"_id": ObjectId(db_provider.id)}, {'$set': db_provider.dict()})

    if updated_at.matched_count != 1:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error persisting provider - id: {id}"
        )

    return db_provider


async def get_providers_paginated(conn: AsyncIOMotorClient, params: LimitOffsetParams) \
        -> LimitOffsetPage[EmbeddedProviderInDB]:
    total_count = await conn[database_name][providers_collection_name].estimated_document_count()
    print(params)

    providers = await conn[database_name][providers_collection_name].find().sort([('_id', 1)]) \
        .skip(params.offset).limit(params.limit).to_list(length=params.limit)

    if providers:
        providers_in_db = {'providers': providers}
        output = ProvidersInDB(**providers_in_db)

        list_of_providers = LimitOffsetPage.create(output.providers, total_count, params)
    else:
        list_of_providers = LimitOffsetPage.create([], total_count, params)

    return list_of_providers
