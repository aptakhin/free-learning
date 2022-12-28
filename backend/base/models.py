"""."""
from datetime import datetime
from typing import Any, Optional

from pydantic import Field, BaseModel


class BaseElement(BaseModel):
    """."""

    typ: str = Field(..., title='Fully-qualified type')
    id: str | None = Field(title='Identifier')
    version: int | None = Field(title='Element version')

    time_created: datetime | None = Field(title='Time created')
    time_updated: datetime | None = Field(title='Time updated')


class Entity(BaseElement):
    """."""

    properties: dict[str, Any] = {}

    class Config(object):
        """."""

        allow_population_by_field_name = True
        schema_extra = {
            'example': {
                'subject_id': '1234',
            },
        }
        json_encoders = {
        }


class EntityUpsertResult(BaseModel):
    """."""

    id: int


class Link(BaseElement):
    """."""

    start_id: int
    end_id: int

    text: str


class LinkUpsertResult(BaseModel):
    """."""

    id: int


class Rule(BaseElement):
    """."""


class EntityQuery(BaseModel):
    """."""

    start_entity_id: Optional[str] = None
    start_entity_label: Optional[str] = None
    start_entity_properties: Optional[dict] = None
    link_label: Optional[str] = None
    link_properties: Optional[dict] = None
    end_entity_id: Optional[str] = None
    end_entity_label: Optional[str] = None
    end_entity_properties: Optional[dict] = None


class EntityQueryResult(BaseModel):
    """."""

    query_result: list
