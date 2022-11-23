from typing import Dict, Optional, List, Union

from pydantic import BaseModel, Field, validator, root_validator

accepted_versions = ["2.0"]


class SDLBaseModel(BaseModel):
    pass


class Cpu(SDLBaseModel):
    units: str


class Memory(SDLBaseModel):
    size: str


class Storage(SDLBaseModel):
    size: str


class ProfileResource(SDLBaseModel):
    cpu: Optional[Cpu]
    memory: Optional[Memory]
    storage: Union[Optional[Storage], Optional[List[Dict]]]


class Resources(SDLBaseModel):
    resources: ProfileResource


class ServiceExposeTo(SDLBaseModel):
    service: Optional[str] = None
    global_: Optional[bool] = Field(default=None, alias="global")


class ServiceExpose(SDLBaseModel):
    port: int
    as_: Optional[int] = Field(default=None, alias="as")
    accept: Optional[List[str]]
    proto: Optional[str]
    to_: List[ServiceExposeTo] = Field(default=None, alias="to")


class Service(SDLBaseModel):
    image: str
    depends_on: Optional[str] = Field(default=None, alias="depends-on")
    command: Optional[str] = None
    args: Optional[str] = None
    env: Optional[List[Dict[str, str]]] = None
    expose: Optional[List[ServiceExpose]] = None


class ProfilePlacementAttrs(SDLBaseModel):
    region: str


class ProfilePlacement(SDLBaseModel):
    attributes: ProfilePlacementAttrs
    signed_by: Optional[Dict] = Field(default=None, alias="signedBy")
    pricing: Optional[Dict]


class Profiles(SDLBaseModel):
    compute: Dict[str, Resources]
    placement: Dict[str, ProfilePlacement]

    def get_compute_services(self):
        return self.compute.keys()


class DeploymentConfig(SDLBaseModel):
    profile: Optional[str]
    count: Optional[int]


class SDLModel(SDLBaseModel):
    version: str
    services: Dict[str, Service]
    profiles: Profiles
    deployment: Optional[Dict[str, Dict[str, DeploymentConfig]]]

    def get_services(self):
        return self.services.keys()

    @validator('version')
    def name_must_contain_space(cls, v):
        if v not in accepted_versions:
            raise ValueError('version is invalid!')
        return v.title()

    @root_validator
    def profile_compute_service_matches_services(cls, values):
        if values.get('profiles').compute.keys().isdisjoint(values.get('services').keys()):
            raise ValueError('service name mismatch! -> profiles')
        if values.get('deployment').keys().isdisjoint(values.get('services').keys()):
            raise ValueError('service name mismatch! -> deployment')
        return values
