"""."""

import logging
from fastapi import APIRouter, Depends
from base.db_age import make_properties, make_label, dumps as age_dumps, loads as age_loads
from base.db import get_db
from base.models import Entity, EntityUpsertResult, Link, LinkUpsertResult


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
    label = make_label(entity.typ)
    properties = make_properties(entity.dict(exclude_none=True, exclude={'typ'}))
    query = f"""SELECT * FROM cypher('msft', $$
        CREATE (a :{label} {properties})
        RETURN a
    $$) as (a agtype);"""

    print(db, type(db))
    logger.debug('Insert link query:', query)
    async with db._engine.begin() as conn:
        from sqlalchemy.sql import text
        result = await conn.execute(text(query))
        result_raw, = result.one()
        result_row = age_loads(result_raw)
        print('X', result, result_row, type(result_row))
    # result_row = await db.fetchval(query)
    logger.debug('Insert link query result:', result_row)

    return EntityUpsertResult(
        id=result_row['id'],
    )


@router.post('/upsert-link', response_model=LinkUpsertResult)
async def upsert_link(
    link: Link,
    db=Depends(get_db),  # noqa: B008, WPS404
) -> LinkUpsertResult:
    """Upserts link."""
    label = make_label(link.typ)
    properties = make_properties(link.dict(exclude_none=True, exclude={'typ', 'start_id', 'end_id'}))
    query = f"""SELECT * FROM cypher('msft', $$
        MATCH (a), (b)
        WHERE id(a) = {link.start_id} AND id(b) = {link.end_id}
        CREATE (a)-[e :{label} {properties}]->(b)
        RETURN e
    $$) as (items agtype);"""
    logger.debug('Insert link query:', query)
    async with db._engine.begin() as conn:
        from sqlalchemy.sql import text
        result = await conn.execute(text(query))
        result_raw, = result.one()
        result_row = age_loads(result_raw)
        print('X', result, result_row, type(result_row))
    logger.debug('Insert link query result:', result_row)

    return LinkUpsertResult(
        id=result_row['id'],
    )
