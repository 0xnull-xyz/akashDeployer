from fastapi import APIRouter, Body, Depends
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.security.jwt import allowed_create_base_resources, allowed_access_base_resources, \
    get_current_user_authorizer
from app.crud.deployment_type import create_deployment_type, update_deployment_type, get_deployment_types_paginated
from app.crud.shortcuts import check_free_deployment_type_title
from app.db.mongodb import get_database
from app.models.deployment_type import EmbeddedDeploymentTypeInDB, DeploymentTypeInResponse, DeploymentTypeInCreate, \
    DeploymentTypeInUpdate
from app.models.shared import LimitOffsetPage, LimitOffsetParams
from app.models.user import User

router = APIRouter()


@router.post("/deployment_type", response_model=DeploymentTypeInResponse, tags=["deployment_types"])
async def create_deployment_type(
        deployment_type: DeploymentTypeInCreate = Body(..., embed=True),
        db: AsyncIOMotorClient = Depends(get_database),
        dependencies=Depends(allowed_create_base_resources),
):
    await check_free_deployment_type_title(db, deployment_type.title)

    async with await db.start_session() as s:
        async with s.start_transaction():
            db_deployment_type = await create_deployment_type(db, deployment_type)

            return DeploymentTypeInResponse(deployment_type=db_deployment_type)


@router.put("/deployment_type", response_model=DeploymentTypeInResponse, tags=["deployment_types"])
async def update_deployment_type(
        deployment_type: DeploymentTypeInUpdate = Body(..., embed=True),
        db: AsyncIOMotorClient = Depends(get_database),
        dependencies=Depends(allowed_create_base_resources),
):
    async with await db.start_session() as s:
        async with s.start_transaction():
            db_deployment_type = await update_deployment_type(db, deployment_type.id, deployment_type)

            return DeploymentTypeInResponse(deployment_type=db_deployment_type)


@router.get("/deployment_type", response_model=LimitOffsetPage[EmbeddedDeploymentTypeInDB],
            tags=["deployment_types"])
async def get_deployment_types(
        skip: int = 0, limit: int = 10,
        db: AsyncIOMotorClient = Depends(get_database),
        dependencies=Depends(allowed_access_base_resources),
):
    params = LimitOffsetParams(**{'offset': skip, 'limit': limit})
    async with await db.start_session() as db_apps:
        async with db_apps.start_transaction():
            db_apps = await get_deployment_types_paginated(db, params)

            return db_apps


@router.get("/deployment_type/my", response_model=LimitOffsetPage[EmbeddedDeploymentTypeInDB],
            tags=["deployment_types"])
async def get_my_deployment_types(
        skip: int = 0, limit: int = 10,
        db: AsyncIOMotorClient = Depends(get_database),
        user: User = Depends(get_current_user_authorizer(required=True)),
):
    params = LimitOffsetParams(**{'offset': skip, 'limit': limit})
    async with await db.start_session() as db_apps:
        async with db_apps.start_transaction():
            db_apps = await get_deployment_types_paginated(db, params, user.id)

            return db_apps
