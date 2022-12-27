"""."""

import logging
from typing import Optional

from base.db import get_db
from base.models import Entity, EntityUpsertResult, Link, LinkUpsertResult, EntityQueryResult, EntityQuery
from fastapi import APIRouter, Depends


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/api/{FL_MODULE_BASE}/v1',
    tags=['base'],
    responses={404: {'description': 'Not found'}},
)


@router.post('/upsert-entity', response_model=EntityUpsertResult)
async def upsert_entity(
    entity: Entity,
    db=Depends(get_db),  # noqa: B008, WPS404
) -> EntityUpsertResult:
    """Upserts entity."""
    result_row = await db.upsert_entity(entity)
    return EntityUpsertResult(
        id=result_row['id'],
    )


@router.get('/query-linked/', response_model=EntityQueryResult)
async def query_linked(
    start_entity_id: Optional[int] = None,
    start_entity_label: Optional[str] = None,
    start_entity_properties: Optional[dict] = None,
    link_label: Optional[str] = None,
    link_properties: Optional[dict] = None,
    end_entity_id: Optional[int] = None,
    end_entity_label: Optional[str] = None,
    end_entity_properties: Optional[dict] = None,
    db=Depends(get_db),  # noqa: B008, WPS404
) -> EntityQueryResult:
    """Query entity."""
    result = await db.query_linked(
        start_entity_id=start_entity_id,
        start_entity_label=start_entity_label,
        start_entity_properties=start_entity_properties,
        link_label=link_label,
        link_properties=link_properties,
        end_entity_id=end_entity_id,
        end_entity_label=end_entity_label,
        end_entity_properties=end_entity_properties,
    )
    return EntityQueryResult(
        result=result,
    )


@router.post('/upsert-link', response_model=LinkUpsertResult)
async def upsert_link(
    link: Link,
    db=Depends(get_db),  # noqa: B008, WPS404
) -> LinkUpsertResult:
    """Upserts link."""
    result_row = await db.upsert_link(link)
    return LinkUpsertResult(
        id=result_row['id'],
    )
