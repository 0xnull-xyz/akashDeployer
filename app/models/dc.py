from typing import Optional, List

from pydantic import Field

from .dbmodel import DBModelMixin, EmbeddedDBModelMixin
from .rwmodel import RWModel, EmbeddedRWModel


class DCBase(RWModel):
    title: str = Field(..., min_length=3)
    region: str = Field(..., min_length=24)
    desc: Optional[str]


class EmbeddedDCBase(EmbeddedRWModel):
    title: str = Field(..., min_length=3)
    region: str = Field(..., min_length=24)
    desc: Optional[str]


class EmbeddedDCInDB(EmbeddedDBModelMixin, EmbeddedDCBase):
    pass


class DCInDB(DBModelMixin, DCBase):
    pass


class DCsInDB(EmbeddedRWModel):
    DCs: List[EmbeddedDCInDB]


class DC(DCBase):
    pass


class DCInResponse(RWModel):
    DC: DC


class DCInCreate(DCBase):
    pass


class DCInUpdate(EmbeddedDCInDB):
    pass
