from typing import Optional, List

from pydantic import Field

from .dbmodel import DBModelMixin, EmbeddedDBModelMixin
from .rwmodel import RWModel, EmbeddedRWModel


class DeploymentTypeBase(RWModel):
    title: str = Field(..., min_length=3)
    desc: Optional[str]
    image_url: Optional[str]
    owner_id: str = Field(..., min_length=24)


class EmbeddedDeploymentTypeBase(EmbeddedRWModel):
    title: str = Field(..., min_length=3)
    desc: Optional[str]
    image_url: Optional[str]
    owner_id: str = Field(..., min_length=24)


class EmbeddedDeploymentTypeInDB(EmbeddedDBModelMixin, EmbeddedDeploymentTypeBase):
    pass


class DeploymentTypeInDB(DBModelMixin, DeploymentTypeBase):
    pass


class DeploymentTypesInDB(EmbeddedRWModel):
    DeploymentTypes: List[EmbeddedDeploymentTypeInDB]


class DeploymentType(DeploymentTypeBase):
    pass


class DeploymentTypeInResponse(RWModel):
    DeploymentType: DeploymentType


class DeploymentTypeInCreate(DeploymentTypeBase):
    pass


class DeploymentTypeInUpdate(EmbeddedDeploymentTypeInDB):
    pass
