from typing import Optional, List

from pydantic import Field

from .dbmodel import DBModelMixin, EmbeddedDBModelMixin
from .rwmodel import RWModel, EmbeddedRWModel


class ProviderBase(RWModel):
    title: str = Field(..., min_length=3)
    desc: Optional[str]
    image_url: Optional[str]


class EmbeddedProviderBase(EmbeddedRWModel):
    title: str = Field(..., min_length=3)
    desc: Optional[str]
    image_url: Optional[str]


class EmbeddedProviderInDB(EmbeddedDBModelMixin, EmbeddedProviderBase):
    pass


class ProviderInDB(DBModelMixin, ProviderBase):
    pass


class ProvidersInDB(EmbeddedRWModel):
    Providers: List[EmbeddedProviderInDB]


class Provider(ProviderBase):
    pass


class ProviderInResponse(RWModel):
    Provider: Provider


class ProviderInCreate(ProviderBase):
    pass


class ProviderInUpdate(EmbeddedProviderInDB):
    pass
