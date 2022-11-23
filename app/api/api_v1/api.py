from fastapi import APIRouter

from app.api.api_v1.endpoints.authenticaion import router as auth_router
from app.api.api_v1.endpoints.dc import router as dc_router
from app.api.api_v1.endpoints.deployment import router as deployment_router
from app.api.api_v1.endpoints.deployment_definition import router as deployment_definition_router
from app.api.api_v1.endpoints.deployment_type import router as deployment_type_router
from app.api.api_v1.endpoints.profile import router as profile_router
from app.api.api_v1.endpoints.provider import router as provider_router
from app.api.api_v1.endpoints.region import router as region_router
from app.api.api_v1.endpoints.sdl import router as sdl_router
from app.api.api_v1.endpoints.sdl_template import router as sdl_template_router
from app.api.api_v1.endpoints.tag import router as tag_router
from app.api.api_v1.endpoints.user import router as user_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(user_router)
router.include_router(profile_router)
router.include_router(tag_router)
router.include_router(sdl_router)
router.include_router(dc_router)
router.include_router(deployment_router)
router.include_router(deployment_definition_router)
router.include_router(deployment_type_router)
router.include_router(provider_router)
router.include_router(region_router)
router.include_router(sdl_template_router)
