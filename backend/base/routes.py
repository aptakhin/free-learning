"""."""

from fastapi import APIRouter, Depends
from base.config import Settings, FL_MODULE_BASE
from base.db_age import make_properties, make_label
from base.db import get_db
from base.models import Entity, EntityUpsertResult, Link, LinkUpsertResult


router = APIRouter(
    prefix='/api/{FL_MODULE_BASE}/v1',
    tags=['base'],
    responses={404: {'description': 'Not found'}},
)

@router.post('/upsert-entity', response_model=EntityUpsertResult)
async def upsert_entity(
    entity: Entity,
    db=Depends(get_db),  # noqa: B008
) -> EntityUpsertResult:
    """Upserts entity."""
    label = make_label(entity.typ)
    properties = make_properties(entity.dict(exclude_none=True, exclude={'typ'}))
    QUERY = f"""SELECT * FROM cypher('msft', $$
        CREATE (a :{label} {properties})
        RETURN a
    $$) as (a agtype);"""
    result_row = await db.fetchval(QUERY)
    print(result_row, 'X')
    return EntityUpsertResult(
        id=result_row['id'],
    )


@router.post('/upsert-link', response_model=LinkUpsertResult)
async def upsert_link(
    link: Link,
    db=Depends(get_db),  # noqa: B008
) -> LinkUpsertResult:
    """Upserts link."""

    label = make_label(link.typ)
    properties = make_properties(link.dict(exclude_none=True, exclude={'typ', 'start_id', 'end_id'}))
 # :`com.freelearning.hello`
    QUERY = f"""SELECT * FROM cypher('msft', $$
        MATCH (a), (b)
        WHERE a.fid = '{link.start_id}' AND b.fid = '{link.end_id}'
        CREATE (a)-[e :HELLO {properties}]->(b)
        RETURN e
    $$) as (items agtype);"""
    print(QUERY)
    result_row = await db.fetchval(QUERY)
    print(result_row)

    return LinkUpsertResult(
        id=result_row['id'],
    )
