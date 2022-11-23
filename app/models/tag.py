from typing import Optional, List

from pydantic import Field

from .dbmodel import DBModelMixin, EmbeddedDBModelMixin
from .rwmodel import RWModel, EmbeddedRWModel


class TagBase(RWModel):
    title: str = Field(..., min_length=3)
    desc: Optional[str]
    image_url: Optional[str]
    owner_id: str = Field(..., min_length=24)


class EmbeddedTagBase(EmbeddedRWModel):
    title: str = Field(..., min_length=3)
    desc: Optional[str]
    image_url: Optional[str]
    owner_id: str = Field(..., min_length=24)


class EmbeddedTagInDB(EmbeddedDBModelMixin, EmbeddedTagBase):
    pass


class TagInDB(DBModelMixin, TagBase):
    pass


class TagsInDB(EmbeddedRWModel):
    tags: List[EmbeddedTagInDB]


class Tag(TagBase):
    pass


class TagInResponse(RWModel):
    tag: Tag


class TagInCreate(TagBase):
    pass


class TagInUpdate(EmbeddedTagInDB):
    pass
