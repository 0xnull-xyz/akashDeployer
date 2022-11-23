from typing import Optional

from starlette.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from app.crud.user import get_user
from app.db.mongodb import AsyncIOMotorClient
from app.models.profile import Profile


async def get_profile_for_user(
        conn: AsyncIOMotorClient, target_username: str, current_username: Optional[str] = None
) -> Profile:
    user = await get_user(conn, target_username)
    if not user:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail=f"User {target_username} not found"
        )

    profile = Profile(**user.dict())

    return profile
