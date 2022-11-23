from datetime import datetime
from typing import Optional, List

from pydantic import Field, validator

from .dbmodel import DBModelMixin, EmbeddedDBModelMixin
from .deployment_type import EmbeddedDeploymentTypeInDB
from .rwmodel import RWModel, EmbeddedRWModel, BaseRWModel
from .tag import EmbeddedTagInDB

accepted_deployers = ['AkashDeployer']


class DeploymentResource(BaseRWModel):
    cpu: Optional[str]
    memory: Optional[str]
    ephemeral_storage: Optional[str]
    persistent_storage: Optional[str]


class DeploymentBase(RWModel):
    region_id: str = Field(..., min_length=24)
    dc_id: str = Field(..., min_length=24)
    provider_id: Optional[str] = ""
    title: str = Field(..., min_length=3)
    resources: List[DeploymentResource]
    desc: Optional[str]
    owner_id: str = Field(..., min_length=24)
    deployer_id: str = Field(..., min_length=3)
    is_payment_managed: Optional[bool]
    installed_at: Optional[datetime] = None
    uninstalled_at: Optional[datetime] = None

    @validator('deployer_id')
    def name_must_contain_space(cls, v):
        if v not in accepted_deployers:
            raise ValueError('deployer is invalid!')
        return v.title()


class EmbeddedDeploymentBase(EmbeddedRWModel):
    region_id: str = Field(..., min_length=24)
    dc_id: str = Field(..., min_length=24)
    provider_id: Optional[str] = ""
    title: str = Field(..., min_length=3)
    desc: Optional[str]
    owner_id: str = Field(..., min_length=24)
    deployer_id: str = Field(..., min_length=3)
    installed_at: Optional[datetime] = None
    uninstalled_at: Optional[datetime] = None


class EmbeddedDeploymentInDB(EmbeddedDBModelMixin, EmbeddedDeploymentBase):
    deployment_type: EmbeddedDeploymentTypeInDB
    tags: List[EmbeddedTagInDB]


class DeploymentInDB(DBModelMixin, DeploymentBase):
    pass


class DeploymentsInDB(EmbeddedRWModel):
    Deployments: List[EmbeddedDeploymentInDB]


class Deployment(DeploymentBase):
    deployment_type: EmbeddedDeploymentTypeInDB
    tags: List[EmbeddedTagInDB]


class DeploymentInResponse(RWModel):
    Deployment: Deployment


class DeploymentInCreate(DeploymentBase):
    deployment_type: str = Field(..., min_length=10)
    tags: List[str]
    pass


class DeploymentInUpdate(EmbeddedDeploymentInDB):
    deployment_type: str = Field(..., min_length=10)
    tags: List[str]
    pass
