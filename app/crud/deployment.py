import datetime
from typing import Optional

from bson.objectid import ObjectId
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from app.core.configs.config import database_name, deployments_collection_name
from app.db.mongodb import AsyncIOMotorClient
from app.models.deployment import DeploymentInCreate, DeploymentInDB, DeploymentInUpdate, EmbeddedDeploymentInDB, \
    DeploymentsInDB
from app.models.shared import LimitOffsetParams, LimitOffsetPage


async def get_deployment(conn: AsyncIOMotorClient, title: str) -> Optional[DeploymentInDB]:
    row = await conn[database_name][deployments_collection_name].find_one({"title": title})
    if row:
        return DeploymentInDB(**row)


# noinspection PyShadowingBuiltins
async def get_deployment_by_id(conn: AsyncIOMotorClient, id: str) -> Optional[DeploymentInDB]:
    try:
        row = await conn[database_name][deployments_collection_name].find_one({"_id": ObjectId(id)})
        if row:
            return DeploymentInDB(**row)
    except Exception as e:
        # @254: log
        return None


async def create_deployment(conn: AsyncIOMotorClient, deployment: DeploymentInCreate) -> DeploymentInDB:
    db_deployment = DeploymentInDB(**deployment.dict())

    row = await conn[database_name][deployments_collection_name].insert_one(db_deployment.dict())

    db_deployment.id = row.inserted_id

    return db_deployment


async def update_deployment(conn: AsyncIOMotorClient, id: str, deployment: DeploymentInUpdate) -> DeploymentInDB:
    db_deployment = await get_deployment_by_id(conn, id)
    if not db_deployment:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Incorrect deployment id"
        )

    db_deployment.title = deployment.title or db_deployment.title
    db_deployment.desc = deployment.desc or db_deployment.desc
    db_deployment.updated_at = datetime.datetime.utcnow()

    updated_at = await conn[database_name][deployments_collection_name] \
        .update_one({"_id": ObjectId(db_deployment.id)}, {'$set': db_deployment.dict()})

    if updated_at.matched_count != 1:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error persisting deployment - id: {id}"
        )

    return db_deployment


async def get_deployments_paginated(conn: AsyncIOMotorClient, params: LimitOffsetParams,
                                    owner_id: str = None) \
        -> LimitOffsetPage[EmbeddedDeploymentInDB]:
    total_count = await conn[database_name][deployments_collection_name].estimated_document_count()
    print(params)

    if owner_id:
        deployments = await conn[database_name][deployments_collection_name] \
            .find({"owner_id": owner_id}).sort([('_id', 1)]) \
            .skip(params.offset).limit(params.limit).to_list(length=params.limit)
    else:
        deployments = await conn[database_name][deployments_collection_name].find().sort([('_id', 1)]) \
            .skip(params.offset).limit(params.limit).to_list(length=params.limit)

    if deployments:
        deployments_in_db = {'deployments': deployments}
        output = DeploymentsInDB(**deployments_in_db)

        list_of_deployments = LimitOffsetPage.create(output.deployments, total_count, params)
    else:
        list_of_deployments = LimitOffsetPage.create([], total_count, params)

    return list_of_deployments
