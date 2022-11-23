import datetime
from typing import Optional

from bson.objectid import ObjectId
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from app.core.configs.config import database_name, deployment_types_collection_name
from app.db.mongodb import AsyncIOMotorClient
from app.models.deployment_type import DeploymentTypeInCreate, DeploymentTypeInDB, DeploymentTypeInUpdate, \
    EmbeddedDeploymentTypeInDB, DeploymentTypesInDB
from app.models.shared import LimitOffsetParams, LimitOffsetPage


async def get_deployment_type(conn: AsyncIOMotorClient, title: str) -> Optional[DeploymentTypeInDB]:
    row = await conn[database_name][deployment_types_collection_name].find_one({"title": title})
    if row:
        return DeploymentTypeInDB(**row)


# noinspection PyShadowingBuiltins
async def get_deployment_type_by_id(conn: AsyncIOMotorClient, id: str) -> Optional[DeploymentTypeInDB]:
    try:
        row = await conn[database_name][deployment_types_collection_name].find_one({"_id": ObjectId(id)})
        if row:
            return DeploymentTypeInDB(**row)
    except Exception as e:
        # @254: log
        return None


async def create_deployment_type(conn: AsyncIOMotorClient,
                                 deployment_type: DeploymentTypeInCreate) -> DeploymentTypeInDB:
    db_deployment_type = DeploymentTypeInDB(**deployment_type.dict())

    row = await conn[database_name][deployment_types_collection_name].insert_one(db_deployment_type.dict())

    db_deployment_type.id = row.inserted_id

    return db_deployment_type


async def update_deployment_type(conn: AsyncIOMotorClient, id: str,
                                 deployment_type: DeploymentTypeInUpdate) -> DeploymentTypeInDB:
    db_deployment_type = await get_deployment_type_by_id(conn, id)
    if not db_deployment_type:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Incorrect deployment_type id"
        )

    db_deployment_type.title = deployment_type.title or db_deployment_type.title
    db_deployment_type.desc = deployment_type.desc or db_deployment_type.desc
    db_deployment_type.updated_at = datetime.datetime.utcnow()

    updated_at = await conn[database_name][deployment_types_collection_name] \
        .update_one({"_id": ObjectId(db_deployment_type.id)}, {'$set': db_deployment_type.dict()})

    if updated_at.matched_count != 1:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error persisting deployment_type - id: {id}"
        )

    return db_deployment_type


async def get_deployment_types_paginated(conn: AsyncIOMotorClient, params: LimitOffsetParams,
                                         owner_id: str = None) \
        -> LimitOffsetPage[EmbeddedDeploymentTypeInDB]:
    total_count = await conn[database_name][deployment_types_collection_name].estimated_document_count()
    print(params)

    if owner_id:
        deployment_types = await conn[database_name][deployment_types_collection_name] \
            .find({"owner_id": owner_id}).sort([('_id', 1)]) \
            .skip(params.offset).limit(params.limit).to_list(length=params.limit)
    else:
        deployment_types = await conn[database_name][deployment_types_collection_name].find().sort([('_id', 1)]) \
            .skip(params.offset).limit(params.limit).to_list(length=params.limit)

    if deployment_types:
        deployment_types_in_db = {'deployment_types': deployment_types}
        output = DeploymentTypesInDB(**deployment_types_in_db)

        list_of_deployment_types = LimitOffsetPage.create(output.deployment_types, total_count, params)
    else:
        list_of_deployment_types = LimitOffsetPage.create([], total_count, params)

    return list_of_deployment_types
