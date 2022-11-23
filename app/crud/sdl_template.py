import datetime
from typing import Optional

from bson.objectid import ObjectId
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from app.core.configs.config import database_name, sdl_templates_collection_name
from app.db.mongodb import AsyncIOMotorClient
from app.models.sdl_template import SDLTemplateInCreate, SDLTemplateInDB, SDLTemplateInUpdate, EmbeddedSDLTemplateInDB, \
    SDLTemplatesInDB
from app.models.shared import LimitOffsetParams, LimitOffsetPage


async def get_sdl_template(conn: AsyncIOMotorClient, title: str) -> Optional[SDLTemplateInDB]:
    row = await conn[database_name][sdl_templates_collection_name].find_one({"title": title})
    if row:
        return SDLTemplateInDB(**row)


# noinspection PyShadowingBuiltins
async def get_sdl_template_by_id(conn: AsyncIOMotorClient, id: str) -> Optional[SDLTemplateInDB]:
    try:
        row = await conn[database_name][sdl_templates_collection_name].find_one({"_id": ObjectId(id)})
        if row:
            return SDLTemplateInDB(**row)
    except Exception as e:
        # @254: log
        return None


async def create_sdl_template(conn: AsyncIOMotorClient, sdl_template: SDLTemplateInCreate) -> SDLTemplateInDB:
    db_sdl_template = SDLTemplateInDB(**sdl_template.dict())

    row = await conn[database_name][sdl_templates_collection_name].insert_one(db_sdl_template.dict())

    db_sdl_template.id = row.inserted_id

    return db_sdl_template


async def update_sdl_template(conn: AsyncIOMotorClient, id: str, sdl_template: SDLTemplateInUpdate) -> SDLTemplateInDB:
    db_sdl_template = await get_sdl_template_by_id(conn, id)
    if not db_sdl_template:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Incorrect sdl_template id"
        )

    db_sdl_template.title = sdl_template.title or db_sdl_template.title
    db_sdl_template.desc = sdl_template.desc or db_sdl_template.desc
    db_sdl_template.updated_at = datetime.datetime.utcnow()

    updated_at = await conn[database_name][sdl_templates_collection_name] \
        .update_one({"_id": ObjectId(db_sdl_template.id)}, {'$set': db_sdl_template.dict()})

    if updated_at.matched_count != 1:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error persisting sdl_template - id: {id}"
        )

    return db_sdl_template


async def get_sdl_templates_paginated(conn: AsyncIOMotorClient, params: LimitOffsetParams) \
        -> LimitOffsetPage[EmbeddedSDLTemplateInDB]:
    total_count = await conn[database_name][sdl_templates_collection_name].estimated_document_count()
    print(params)

    sdl_templates = await conn[database_name][sdl_templates_collection_name].find().sort([('_id', 1)]) \
        .skip(params.offset).limit(params.limit).to_list(length=params.limit)

    if sdl_templates:
        sdl_templates_in_db = {'sdl_templates': sdl_templates}
        output = SDLTemplatesInDB(**sdl_templates_in_db)

        list_of_sdl_templates = LimitOffsetPage.create(output.sdl_templates, total_count, params)
    else:
        list_of_sdl_templates = LimitOffsetPage.create([], total_count, params)

    return list_of_sdl_templates
