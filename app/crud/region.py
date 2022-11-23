import datetime
from typing import Optional

from bson.objectid import ObjectId
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from app.core.configs.config import database_name, regions_collection_name
from app.db.mongodb import AsyncIOMotorClient
from app.models.region import RegionInCreate, RegionInDB, RegionInUpdate, EmbeddedRegionInDB, RegionsInDB
from app.models.shared import LimitOffsetParams, LimitOffsetPage


async def get_region(conn: AsyncIOMotorClient, title: str) -> Optional[RegionInDB]:
    row = await conn[database_name][regions_collection_name].find_one({"title": title})
    if row:
        return RegionInDB(**row)


# noinspection PyShadowingBuiltins
async def get_region_by_id(conn: AsyncIOMotorClient, id: str) -> Optional[RegionInDB]:
    try:
        row = await conn[database_name][regions_collection_name].find_one({"_id": ObjectId(id)})
        if row:
            return RegionInDB(**row)
    except Exception as e:
        # @254: log
        return None


async def create_region(conn: AsyncIOMotorClient, region: RegionInCreate) -> RegionInDB:
    db_region = RegionInDB(**region.dict())

    row = await conn[database_name][regions_collection_name].insert_one(db_region.dict())

    db_region.id = row.inserted_id

    return db_region


async def update_region(conn: AsyncIOMotorClient, id: str, region: RegionInUpdate) -> RegionInDB:
    db_region = await get_region_by_id(conn, id)
    if not db_region:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Incorrect region id"
        )

    db_region.title = region.title or db_region.title
    db_region.desc = region.desc or db_region.desc
    db_region.updated_at = datetime.datetime.utcnow()

    updated_at = await conn[database_name][regions_collection_name] \
        .update_one({"_id": ObjectId(db_region.id)}, {'$set': db_region.dict()})

    if updated_at.matched_count != 1:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error persisting region - id: {id}"
        )

    return db_region


async def get_regions_paginated(conn: AsyncIOMotorClient, params: LimitOffsetParams) \
        -> LimitOffsetPage[EmbeddedRegionInDB]:
    total_count = await conn[database_name][regions_collection_name].estimated_document_count()
    print(params)

    regions = await conn[database_name][regions_collection_name].find().sort([('_id', 1)]) \
        .skip(params.offset).limit(params.limit).to_list(length=params.limit)

    if regions:
        regions_in_db = {'regions': regions}
        output = RegionsInDB(**regions_in_db)

        list_of_regions = LimitOffsetPage.create(output.regions, total_count, params)
    else:
        list_of_regions = LimitOffsetPage.create([], total_count, params)

    return list_of_regions
