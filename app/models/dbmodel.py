from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.py_object_id import PyObjectId


class DateTimeModelMixin(BaseModel):
    created_at: Optional[datetime] = datetime.utcnow()
    updated_at: Optional[datetime] = datetime.utcnow()


class DBModelMixin(DateTimeModelMixin):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")


class EmbeddedDBModelMixin(DateTimeModelMixin):
    id: PyObjectId = Field(..., alias="_id")
