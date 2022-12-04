"""."""
from datetime import datetime
from typing import Optional
import uuid

from pydantic import BaseModel, Field


class Entity(BaseModel):
    """."""

    id: str
    subject_id: str
    time_created: Optional[datetime] = None
    time_updated: Optional[datetime] = None

    class Config(object):
        """."""

        allow_population_by_field_name = True
        schema_extra = {
            'example': {
                '_id': '066de609-b04a-4b30-b46c-32537c7f1f6e',
                # 'subject_id': '123',
            },
        }
        json_encoders = {
            # datetime: lambda v: v.timestamp(),
            # uuid.UUID: str,
        }
