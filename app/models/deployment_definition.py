from typing import Optional, List

from pydantic import Field

from .dbmodel import DBModelMixin, EmbeddedDBModelMixin
from .rwmodel import RWModel, EmbeddedRWModel
from .stack_definition import SDLModel


class DeploymentDefinitionBase(RWModel):
    region_id: str = Field(..., min_length=24)
    dc_id: str = Field(..., min_length=24)
    provider_id: Optional[str] = ""
    owner_id: str = Field(..., min_length=24)
    deployment_id: str = Field(..., min_length=24)
    definition: SDLModel


class EmbeddedDeploymentDefinitionBase(EmbeddedRWModel):
    region_id: str = Field(..., min_length=24)
    dc_id: str = Field(..., min_length=24)
    provider_id: Optional[str] = ""
    owner_id: str = Field(..., min_length=24)
    deployment_id: str = Field(..., min_length=24)
    definition: SDLModel


class EmbeddedDeploymentDefinitionInDB(EmbeddedDBModelMixin, EmbeddedDeploymentDefinitionBase):
    pass


class DeploymentDefinitionInDB(DBModelMixin, DeploymentDefinitionBase):
    pass


class DeploymentDefinitionsInDB(EmbeddedRWModel):
    DeploymentDefinitions: List[EmbeddedDeploymentDefinitionInDB]


class DeploymentDefinition(DeploymentDefinitionBase):
    pass


class DeploymentDefinitionInResponse(RWModel):
    DeploymentDefinition: DeploymentDefinition


class DeploymentDefinitionInCreate(DeploymentDefinitionBase):
    pass


class DeploymentDefinitionInUpdate(EmbeddedDeploymentDefinitionInDB):
    pass
