import datetime
from typing import Optional

from bson.objectid import ObjectId
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from app.core.configs.config import database_name, dcs_collection_name
from app.db.mongodb import AsyncIOMotorClient
from app.models.dc import DCInCreate, DCInDB, DCInUpdate, EmbeddedDCInDB, DCsInDB
from app.models.shared import LimitOffsetParams, LimitOffsetPage


async def get_dc(conn: AsyncIOMotorClient, title: str) -> Optional[DCInDB]:
    row = await conn[database_name][dcs_collection_name].find_one({"title": title})
    if row:
        return DCInDB(**row)


# noinspection PyShadowingBuiltins
async def get_dc_by_id(conn: AsyncIOMotorClient, id: str) -> Optional[DCInDB]:
    try:
        row = await conn[database_name][dcs_collection_name].find_one({"_id": ObjectId(id)})
        if row:
            return DCInDB(**row)
    except Exception as e:
        # @254: log
        return None


async def create_dc(conn: AsyncIOMotorClient, dc: DCInCreate) -> DCInDB:
    db_dc = DCInDB(**dc.dict())

    row = await conn[database_name][dcs_collection_name].insert_one(db_dc.dict())

    db_dc.id = row.inserted_id

    return db_dc


async def update_dc(conn: AsyncIOMotorClient, id: str, dc: DCInUpdate) -> DCInDB:
    db_dc = await get_dc_by_id(conn, id)
    if not db_dc:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Incorrect dc id"
        )

    db_dc.title = dc.title or db_dc.title
    db_dc.desc = dc.desc or db_dc.desc
    db_dc.updated_at = datetime.datetime.utcnow()

    updated_at = await conn[database_name][dcs_collection_name] \
        .update_one({"_id": ObjectId(db_dc.id)}, {'$set': db_dc.dict()})

    if updated_at.matched_count != 1:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error persisting dc - id: {id}"
        )

    return db_dc


async def get_dcs_paginated(conn: AsyncIOMotorClient, params: LimitOffsetParams) \
        -> LimitOffsetPage[EmbeddedDCInDB]:
    total_count = await conn[database_name][dcs_collection_name].estimated_document_count()
    print(params)

    dcs = await conn[database_name][dcs_collection_name].find().sort([('_id', 1)]) \
        .skip(params.offset).limit(params.limit).to_list(length=params.limit)

    if dcs:
        dcs_in_db = {'dcs': dcs}
        output = DCsInDB(**dcs_in_db)

        list_of_dcs = LimitOffsetPage.create(output.dcs, total_count, params)
    else:
        list_of_dcs = LimitOffsetPage.create([], total_count, params)

    return list_of_dcs
