from datetime import datetime, timedelta
from typing import Optional, List

import jwt
from fastapi import Depends, Header
from jwt import PyJWTError
from starlette.exceptions import HTTPException
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from app.core.configs.config import JWT_TOKEN_PREFIX, SECRET_KEY
from app.crud.user import get_user
from app.db.mongodb import AsyncIOMotorClient, get_database
from app.models.token import TokenPayload
from app.models.user import User

ALGORITHM = "HS256"
access_token_jwt_subject = "access"


def _get_authorization_token(authorization: str = Header(...)):
    token_prefix, token = authorization.split(" ")
    if token_prefix != JWT_TOKEN_PREFIX:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Invalid authorization type"
        )

    return token


async def _get_current_user(
        db: AsyncIOMotorClient = Depends(get_database), token: str = Depends(_get_authorization_token)
) -> User:
    try:
        payload = jwt.decode(token, str(SECRET_KEY), algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )

    dbuser = await get_user(db, token_data.username)
    if not dbuser:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")

    user = User(**dbuser.dict(), token=token)
    return user


def _get_authorization_token_optional(authorization: str = Header(None)):
    if authorization:
        return _get_authorization_token(authorization)
    return ""


async def _get_current_user_optional(
        db: AsyncIOMotorClient = Depends(get_database),
        token: str = Depends(_get_authorization_token_optional),
) -> Optional[User]:
    if token:
        return await _get_current_user(db, token)

    return None


def get_current_user_authorizer(*, required: bool = True):
    if required:
        return _get_current_user
    else:
        return _get_current_user_optional


def create_access_token(*, data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire, "sub": access_token_jwt_subject})
    encoded_jwt = jwt.encode(to_encode, str(SECRET_KEY), algorithm=ALGORITHM)
    return encoded_jwt


class RoleChecker:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user_authorizer(required=True))):
        if not set(self.allowed_roles).issubset(set(user.roles)):
            # Logger.debug(f"User with role {user.roles} not in {self.allowed_roles}")
            raise HTTPException(status_code=403, detail="Operation not permitted")


# RBAC configs
allowed_create_base_resources = RoleChecker(["admin"])
allowed_update_base_resources = RoleChecker(["admin"])
allowed_access_base_resources = RoleChecker(["admin"])
allowed_access_public_resources = RoleChecker([])
