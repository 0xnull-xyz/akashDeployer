from fastapi import APIRouter, Body, Depends
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.security.jwt import allowed_create_base_resources, allowed_access_base_resources, \
    get_current_user_authorizer
from app.crud.deployment import create_deployment, update_deployment, get_deployments_paginated
from app.crud.shortcuts import check_free_deployment_title
from app.db.mongodb import get_database
from app.models.deployment import EmbeddedDeploymentInDB, DeploymentInResponse, DeploymentInCreate, DeploymentInUpdate
from app.models.shared import LimitOffsetPage, LimitOffsetParams
from app.models.user import User

router = APIRouter()


@router.post("/deployment", response_model=DeploymentInResponse, tags=["deployments"])
async def create_deployment(
        deployment: DeploymentInCreate = Body(..., embed=True),
        db: AsyncIOMotorClient = Depends(get_database),
        dependencies=Depends(allowed_create_base_resources),
):
    await check_free_deployment_title(db, deployment.title)

    async with await db.start_session() as s:
        async with s.start_transaction():
            db_deployment = await create_deployment(db, deployment)

            return DeploymentInResponse(deployment=db_deployment)


@router.put("/deployment", response_model=DeploymentInResponse, tags=["deployments"])
async def update_deployment(
        deployment: DeploymentInUpdate = Body(..., embed=True),
        db: AsyncIOMotorClient = Depends(get_database),
        dependencies=Depends(allowed_create_base_resources),
):
    async with await db.start_session() as s:
        async with s.start_transaction():
            db_deployment = await update_deployment(db, deployment.id, deployment)

            return DeploymentInResponse(deployment=db_deployment)


@router.get("/deployment", response_model=LimitOffsetPage[EmbeddedDeploymentInDB], tags=["deployments"])
async def get_deployments(
        skip: int = 0, limit: int = 10,
        db: AsyncIOMotorClient = Depends(get_database),
        dependencies=Depends(allowed_access_base_resources),
):
    params = LimitOffsetParams(**{'offset': skip, 'limit': limit})
    async with await db.start_session() as db_apps:
        async with db_apps.start_transaction():
            db_apps = await get_deployments_paginated(db, params)

            return db_apps


@router.get("/deployment/my", response_model=LimitOffsetPage[EmbeddedDeploymentInDB], tags=["deployments"])
async def get_deployments(
        skip: int = 0, limit: int = 10,
        db: AsyncIOMotorClient = Depends(get_database),
        user: User = Depends(get_current_user_authorizer(required=True)),
):
    params = LimitOffsetParams(**{'offset': skip, 'limit': limit})
    async with await db.start_session() as db_apps:
        async with db_apps.start_transaction():
            db_apps = await get_deployments_paginated(db, params, user.id)

            return db_apps
