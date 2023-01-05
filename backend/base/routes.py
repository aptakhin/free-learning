"""."""

import logging

from base.config import FL_MODULE_BASE
from base.db import get_db
from base.models import Entity, EntityUpsertResult, Link, LinkUpsertResult, EntityQueryResult, EntityQuery
from base.view import prepare_view_inplace
from fastapi import APIRouter, Depends

logger = logging.getLogger(__name__)


auth_router = APIRouter(
    prefix='/api/%s/v1' % (FL_MODULE_BASE,),
    tags=['base'],
    responses={404: {'description': 'Not found'}},
)

@auth_router.post('/auth')
async def auth(
    email: str,
    db=Depends(get_db),  # noqa: B008, WPS404
):
    print('HH')


router = APIRouter(
    prefix='/{org_slug}/api/%s/v1' % (FL_MODULE_BASE,),
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


@router.post('/query-linked/', response_model=EntityQueryResult)
async def query_linked(
    query: EntityQuery,
    db=Depends(get_db),  # noqa: B008, WPS404
) -> EntityQueryResult:
    """Query entity."""
    query_result = await db.query_linked(query)

    riched_result = []
    for it in query_result:
        riched_result.append([
            prepare_view_inplace(it[0]),
            it[1],
            prepare_view_inplace(it[2]),
        ])

    riched_result.sort(key=lambda it: it[0]['id'])

    return EntityQueryResult(
        query_result=riched_result,
    )


@router.post('/upsert-link', response_model=LinkUpsertResult)
async def upsert_link(
    link: Link,
    org_slug: str,
    db=Depends(get_db),  # noqa: B008, WPS404
) -> LinkUpsertResult:
    """Upserts link."""
    print('SS', org_slug)
    result_row = await db.upsert_link(link)
    return LinkUpsertResult(
        id=result_row['id'],
    )
