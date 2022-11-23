from typing import Optional

from pydantic import EmailStr

from app.core.security.security import generate_salt, get_password_hash, verify_password
from .dbmodel import DBModelMixin
from .rwmodel import RWModel


class UserBase(RWModel):
    username: str
    email: EmailStr
    wallet_addr: Optional[str] = ""
    bio: Optional[str] = ""
    image: Optional[str] = None
    phone: Optional[str] = ""
    verified: Optional[list] = []
    roles: Optional[list] = []
    device_list: Optional[list] = []


class UserInDB(DBModelMixin, UserBase):
    salt: str = ""
    hashed_password: str = ""

    def check_password(self, password: str):
        return verify_password(self.salt + password, self.hashed_password)

    def change_password(self, password: str):
        self.salt = generate_salt()
        self.hashed_password = get_password_hash(self.salt + password)


class User(UserBase):
    id: str
    token: str


class UserInResponse(RWModel):
    user: User


class UserInLogin(RWModel):
    email: EmailStr
    password: str


class UserInCreate(UserInLogin):
    username: str


class UserInUpdate(RWModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    bio: Optional[str] = None
    image: Optional[str] = None
