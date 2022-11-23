from typing import Optional

from fastapi import APIRouter, Depends, Path

from app.core.security.jwt import get_current_user_authorizer
from app.crud.profile import get_profile_for_user
from app.db.mongodb import AsyncIOMotorClient, get_database
from app.models.profile import ProfileInResponse
from app.models.user import User

router = APIRouter()


@router.get("/profiles/{username}", response_model=ProfileInResponse, tags=["profiles"])
async def retrieve_profile(
        username: str = Path(..., min_length=1),
        user: Optional[User] = Depends(get_current_user_authorizer(required=False)),
        db: AsyncIOMotorClient = Depends(get_database),
):
    profile = await get_profile_for_user(
        db, username, user.username if user else None
    )
    profile = ProfileInResponse(profile=profile)
    return profile
