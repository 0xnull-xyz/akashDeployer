from datetime import datetime, timezone

from bson import ObjectId
from pydantic import BaseConfig, BaseModel

from app.core.configs.config import DEFAULT_MONGO_ENTITY_VER


class BaseRWModel(BaseModel):
    class Config(BaseConfig):
        allow_population_by_alias = True
        # we don't need id to persist if we wanted it in our dict we would've used .dict(include={'id': True,
        json_encoders = {
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc)
            .isoformat()
            .replace("+00:00", "Z")
        }


class RWModel(BaseModel):
    version: str = DEFAULT_MONGO_ENTITY_VER

    class Config(BaseConfig):
        allow_population_by_alias = True
        arbitrary_types_allowed = True
        # we don't need id to persist if we wanted it in our dict we would've used .dict(include={'id': True,
        fields = {'id': {'exclude': True}}
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc)
            .isoformat()
            .replace("+00:00", "Z")
        }


class EmbeddedRWModel(BaseModel):
    version: str = DEFAULT_MONGO_ENTITY_VER

    class Config(BaseConfig):
        allow_population_by_alias = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc)
            .isoformat()
            .replace("+00:00", "Z")
        }
