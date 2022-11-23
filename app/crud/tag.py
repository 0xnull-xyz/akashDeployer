import datetime
from typing import Optional

from bson.objectid import ObjectId
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from app.core.configs.config import database_name, tags_collection_name
from app.db.mongodb import AsyncIOMotorClient
from app.models.shared import LimitOffsetParams, LimitOffsetPage
from app.models.tag import TagInCreate, TagInDB, TagInUpdate, EmbeddedTagInDB, TagsInDB


async def get_tag(conn: AsyncIOMotorClient, title: str) -> Optional[TagInDB]:
    row = await conn[database_name][tags_collection_name].find_one({"title": title})
    if row:
        return TagInDB(**row)


# noinspection PyShadowingBuiltins
async def get_tag_by_id(conn: AsyncIOMotorClient, id: str) -> Optional[TagInDB]:
    try:
        row = await conn[database_name][tags_collection_name].find_one({"_id": ObjectId(id)})
        if row:
            return TagInDB(**row)
    except Exception as e:
        # @254: log
        return None


async def create_tag(conn: AsyncIOMotorClient, tag: TagInCreate) -> TagInDB:
    db_tag = TagInDB(**tag.dict())

    row = await conn[database_name][tags_collection_name].insert_one(db_tag.dict())

    db_tag.id = row.inserted_id

    return db_tag


async def update_tag(conn: AsyncIOMotorClient, id: str, tag: TagInUpdate) -> TagInDB:
    db_tag = await get_tag_by_id(conn, id)
    if not db_tag:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Incorrect tag id"
        )

    db_tag.title = tag.title or db_tag.title
    db_tag.desc = tag.desc or db_tag.desc
    db_tag.updated_at = datetime.datetime.utcnow()

    updated_at = await conn[database_name][tags_collection_name] \
        .update_one({"_id": ObjectId(db_tag.id)}, {'$set': db_tag.dict()})

    if updated_at.matched_count != 1:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error persisting tag - id: {id}"
        )

    return db_tag


async def get_tags_paginated(conn: AsyncIOMotorClient, params: LimitOffsetParams, owner_id: str = None) \
        -> LimitOffsetPage[EmbeddedTagInDB]:
    total_count = await conn[database_name][tags_collection_name].estimated_document_count()
    print(params)

    if owner_id:
        tags = await conn[database_name][tags_collection_name] \
            .find({"owner_id": owner_id}).sort([('_id', 1)]) \
            .skip(params.offset).limit(params.limit).to_list(length=params.limit)
    else:
        tags = await conn[database_name][tags_collection_name].find().sort([('_id', 1)]) \
            .skip(params.offset).limit(params.limit).to_list(length=params.limit)

    if tags:
        tags_in_db = {'tags': tags}
        output = TagsInDB(**tags_in_db)

        list_of_tags = LimitOffsetPage.create(output.tags, total_count, params)
    else:
        list_of_tags = LimitOffsetPage.create([], total_count, params)

    return list_of_tags
