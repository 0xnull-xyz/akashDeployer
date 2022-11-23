from typing import Optional, List

from pydantic import Field

from .dbmodel import DBModelMixin, EmbeddedDBModelMixin
from .rwmodel import RWModel, EmbeddedRWModel


class RegionBase(RWModel):
    title: str = Field(..., min_length=3)
    provider: str = Field(..., min_length=24)
    desc: Optional[str]


class EmbeddedRegionBase(EmbeddedRWModel):
    title: str = Field(..., min_length=3)
    provider: str = Field(..., min_length=24)
    desc: Optional[str]


class EmbeddedRegionInDB(EmbeddedDBModelMixin, EmbeddedRegionBase):
    pass


class RegionInDB(DBModelMixin, RegionBase):
    pass


class RegionsInDB(EmbeddedRWModel):
    Regions: List[EmbeddedRegionInDB]


class Region(RegionBase):
    pass


class RegionInResponse(RWModel):
    Region: Region


class RegionInCreate(RegionBase):
    pass


class RegionInUpdate(EmbeddedRegionInDB):
    pass
