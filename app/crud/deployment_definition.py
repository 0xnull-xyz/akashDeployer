import datetime
from typing import Optional

from bson.objectid import ObjectId
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from app.core.configs.config import database_name, deployment_definitions_collection_name
from app.db.mongodb import AsyncIOMotorClient
from app.models.deployment_definition import DeploymentDefinitionInCreate, DeploymentDefinitionInDB, \
    DeploymentDefinitionInUpdate, EmbeddedDeploymentDefinitionInDB, DeploymentDefinitionsInDB
from app.models.shared import LimitOffsetParams, LimitOffsetPage


async def get_deployment_definition(conn: AsyncIOMotorClient, title: str) -> Optional[DeploymentDefinitionInDB]:
    row = await conn[database_name][deployment_definitions_collection_name].find_one({"title": title})
    if row:
        return DeploymentDefinitionInDB(**row)


# noinspection PyShadowingBuiltins
async def get_deployment_definition_by_id(conn: AsyncIOMotorClient, id: str) -> Optional[DeploymentDefinitionInDB]:
    try:
        row = await conn[database_name][deployment_definitions_collection_name].find_one({"_id": ObjectId(id)})
        if row:
            return DeploymentDefinitionInDB(**row)
    except Exception as e:
        # @254: log
        return None


async def create_deployment_definition(conn: AsyncIOMotorClient,
                                       deployment_definition: DeploymentDefinitionInCreate) -> DeploymentDefinitionInDB:
    db_deployment_definition = DeploymentDefinitionInDB(**deployment_definition.dict())

    row = await conn[database_name][deployment_definitions_collection_name].insert_one(db_deployment_definition.dict())

    db_deployment_definition.id = row.inserted_id

    return db_deployment_definition


async def update_deployment_definition(conn: AsyncIOMotorClient, id: str,
                                       deployment_definition: DeploymentDefinitionInUpdate) -> DeploymentDefinitionInDB:
    db_deployment_definition = await get_deployment_definition_by_id(conn, id)
    if not db_deployment_definition:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Incorrect deployment_definition id"
        )

    db_deployment_definition.title = deployment_definition.title or db_deployment_definition.title
    db_deployment_definition.desc = deployment_definition.desc or db_deployment_definition.desc
    db_deployment_definition.updated_at = datetime.datetime.utcnow()

    updated_at = await conn[database_name][deployment_definitions_collection_name] \
        .update_one({"_id": ObjectId(db_deployment_definition.id)}, {'$set': db_deployment_definition.dict()})

    if updated_at.matched_count != 1:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error persisting deployment_definition - id: {id}"
        )

    return db_deployment_definition


async def get_deployment_definitions_paginated(conn: AsyncIOMotorClient, params: LimitOffsetParams,
                                               owner_id: str = None) \
        -> LimitOffsetPage[EmbeddedDeploymentDefinitionInDB]:
    total_count = await conn[database_name][deployment_definitions_collection_name].estimated_document_count()
    print(params)

    if owner_id:
        deployment_definitions = await conn[database_name][deployment_definitions_collection_name] \
            .find({"owner_id": owner_id}).sort([('_id', 1)]) \
            .skip(params.offset).limit(params.limit).to_list(length=params.limit)
    else:
        deployment_definitions = await conn[database_name][deployment_definitions_collection_name].find().sort(
            [('_id', 1)]) \
            .skip(params.offset).limit(params.limit).to_list(length=params.limit)

    if deployment_definitions:
        deployment_definitions_in_db = {'deployment_definitions': deployment_definitions}
        output = DeploymentDefinitionsInDB(**deployment_definitions_in_db)

        list_of_deployment_definitions = LimitOffsetPage.create(output.deployment_definitions, total_count, params)
    else:
        list_of_deployment_definitions = LimitOffsetPage.create([], total_count, params)

    return list_of_deployment_definitions
