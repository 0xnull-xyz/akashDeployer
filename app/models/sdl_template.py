from typing import Optional, List

from pydantic import Field

from .dbmodel import DBModelMixin, EmbeddedDBModelMixin
from .rwmodel import RWModel, EmbeddedRWModel
from .stack_definition import SDLModel


class SDLTemplateBase(RWModel):
    title: str = Field(..., min_length=3)
    desc: Optional[str]
    definition: SDLModel


class EmbeddedSDLTemplateBase(EmbeddedRWModel):
    title: str = Field(..., min_length=3)
    desc: Optional[str]
    definition: SDLModel


class EmbeddedSDLTemplateInDB(EmbeddedDBModelMixin, EmbeddedSDLTemplateBase):
    pass


class SDLTemplateInDB(DBModelMixin, SDLTemplateBase):
    pass


class SDLTemplatesInDB(EmbeddedRWModel):
    SDLTemplates: List[EmbeddedSDLTemplateInDB]


class SDLTemplate(SDLTemplateBase):
    pass


class SDLTemplateInResponse(RWModel):
    SDLTemplate: SDLTemplate


class SDLTemplateInCreate(SDLTemplateBase):
    pass


class SDLTemplateInUpdate(EmbeddedSDLTemplateInDB):
    pass
