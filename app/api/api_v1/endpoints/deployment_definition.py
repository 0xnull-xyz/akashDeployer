from fastapi import APIRouter, Body, Depends
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.security.jwt import allowed_create_base_resources, allowed_access_base_resources, \
    get_current_user_authorizer
from app.crud.deployment_definition import create_deployment_definition, update_deployment_definition, \
    get_deployment_definitions_paginated
from app.db.mongodb import get_database
from app.models.deployment_definition import EmbeddedDeploymentDefinitionInDB, DeploymentDefinitionInResponse, \
    DeploymentDefinitionInCreate, DeploymentDefinitionInUpdate
from app.models.shared import LimitOffsetPage, LimitOffsetParams
from app.models.user import User

router = APIRouter()


@router.post("/deployment_definition", response_model=DeploymentDefinitionInResponse,
             tags=["deployment_definitions"])
async def create_deployment_definition(
        deployment_definition: DeploymentDefinitionInCreate = Body(..., embed=True),
        db: AsyncIOMotorClient = Depends(get_database),
        dependencies=Depends(allowed_create_base_resources),
):
    async with await db.start_session() as s:
        async with s.start_transaction():
            db_deployment_definition = await create_deployment_definition(db, deployment_definition)

            return DeploymentDefinitionInResponse(deployment_definition=db_deployment_definition)


@router.put("/deployment_definition", response_model=DeploymentDefinitionInResponse,
            tags=["deployment_definitions"])
async def update_deployment_definition(
        deployment_definition: DeploymentDefinitionInUpdate = Body(..., embed=True),
        db: AsyncIOMotorClient = Depends(get_database),
        dependencies=Depends(allowed_create_base_resources),
):
    async with await db.start_session() as s:
        async with s.start_transaction():
            db_deployment_definition = await update_deployment_definition(db, deployment_definition.id,
                                                                          deployment_definition)

            return DeploymentDefinitionInResponse(deployment_definition=db_deployment_definition)


@router.get("/deployment_definition", response_model=LimitOffsetPage[EmbeddedDeploymentDefinitionInDB],
            tags=["deployment_definitions"])
async def get_deployment_definitions(
        skip: int = 0, limit: int = 10,
        db: AsyncIOMotorClient = Depends(get_database),
        dependencies=Depends(allowed_access_base_resources),
):
    params = LimitOffsetParams(**{'offset': skip, 'limit': limit})
    async with await db.start_session() as db_apps:
        async with db_apps.start_transaction():
            db_apps = await get_deployment_definitions_paginated(db, params)

            return db_apps


@router.get("/deployment_definition/my", response_model=LimitOffsetPage[EmbeddedDeploymentDefinitionInDB],
            tags=["deployment_definitions"])
async def get_my_deployment_definitions(
        skip: int = 0, limit: int = 10,
        db: AsyncIOMotorClient = Depends(get_database),
        user: User = Depends(get_current_user_authorizer(required=True)),
):
    params = LimitOffsetParams(**{'offset': skip, 'limit': limit})
    async with await db.start_session() as db_apps:
        async with db_apps.start_transaction():
            db_apps = await get_deployment_definitions_paginated(db, params, user.id)

            return db_apps
