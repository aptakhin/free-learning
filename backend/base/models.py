"""."""
from datetime import datetime
from typing import Optional
import uuid

from pydantic import Field, BaseModel
from pydantic.dataclasses import dataclass
from dataclasses import field


# @dataclass
class Entity(BaseModel):
    """."""

    typ: str
    id: str | None
    time_created: datetime | None = Field(title='Time created')
    # time_updated: datetime | None = Field(..., title='The height in cm', ge=50, le=300)

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


# @dataclass
class EntityUpsertResult(BaseModel):
    """."""

    id: str
