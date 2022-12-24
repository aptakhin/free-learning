"""."""
from datetime import datetime

from pydantic import Extra, Field, BaseModel


class BaseElement(BaseModel):
    """."""

    typ: str
    id: str | None
    version: int | None

    time_created: datetime | None = Field(title='Time created')
    time_updated: datetime | None = Field(title='Time created')


class Entity(BaseElement):
    """."""

    typ: str
    id: int | None
    subject_id: str | None
    time_created: datetime | None = Field(title='Time created')

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
        }


class EntityUpsertResult(BaseModel):
    """."""

    id: int


class Link(BaseElement):
    """."""

    start_id: int
    end_id: int

    class Config(object):
        extra = Extra.forbid

class LinkUpsertResult(BaseModel):
    """."""

    id: int
