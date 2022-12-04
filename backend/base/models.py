"""."""
from datetime import datetime
from typing import Optional
import uuid

from pymongo.results import InsertOneResult
from pydantic import BaseModel, Field


class Entity(BaseModel):
    """."""

    id: str | None
    subject_id: str
    time_created: datetime | None # = Field(default_factory=datetime.utcnow)
    time_updated: datetime | None # = Field(default_factory=datetime.utcnow)

    def insert_dict(self) -> dict:
        make_insert_dict = self.dict()
        return make_insert_dict

    class Config(object):
        """."""

        allow_population_by_field_name = True
        schema_extra = {
            'example': {
                'subject_id': '1234',
            },
        }
        json_encoders = {
            datetime: lambda v: v.timestamp(),
            # uuid.UUID: str,
        }


class EntityUpsertResult(BaseModel):
    """."""

    id: str
