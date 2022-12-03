"""."""
import uuid

from pydantic import BaseModel, Field


class FItem(BaseModel):
    """."""

    id: str = Field(default_factory=uuid.uuid4, alias='_id')
    subject_id: str = Field(...)
    time_created: str = Field(...)
    time_updated: str = Field(...)

    class Config(object):
        """."""

        allow_population_by_field_name = True
        schema_extra = {
            'example': {
                '_id': '066de609-b04a-4b30-b46c-32537c7f1f6e',
                'subject_id': '123',
            },
        }
