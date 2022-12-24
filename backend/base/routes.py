"""."""

from fastapi import APIRouter, Depends
from base.config import Settings, FL_MODULE_BASE
from base.db_age import make_properties
from base.db import get_db
from base.models import Entity, EntityUpsertResult


router = APIRouter(
    prefix='/api/{FL_MODULE_BASE}/v1',
    tags=['base'],
    responses={404: {'description': 'Not found'}},
)

@router.post('/upsert-entity', response_model=EntityUpsertResult)
async def upsert_entity(
    entity: Entity,
    db=Depends(get_db),  # noqa: B008
):
    """Upserts entity."""
    # result = await db.entities.insert_one(entity.insert_dict())
    # db =

    labels = ''
    properties = make_properties(entity.dict(exclude_none=True))
    QUERY = f"""SELECT *
FROM cypher('msft', $$
    CREATE (a {properties})
    RETURN a
$$) as (a agtype);"""
    print(QUERY)
    result = await db.fetchval(QUERY)

    print(result)
    return result

    # with db.session(database='msft', fetch_size=100) as session:
    #     result = session.run('MATCH (a:Director) RETURN a.name AS name')
    # # do something with the result...
    #     print(result.single())
    #     # return EntityUpsertResult(id=str(result.inserted_id))
