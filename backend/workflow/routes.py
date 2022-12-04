"""."""

from fastapi import APIRouter, Depends
from base.models import Entity, EntityUpsertResult
from base.config import Settings
from base.db import get_db

router = APIRouter(
    prefix='/api/v1/workflow',
    tags=['workflow'],
    responses={404: {'description': 'Not found'}},
)


@router.post('/{org}/upsert-entity', response_model=EntityUpsertResult)
async def upsert_entity(
    entity: Entity,
    org: str,
    db=Depends(get_db),  # noqa: B008
):
    """Upserts entity."""
    result = await db.entities.insert_one(entity.insert_dict())
    return EntityUpsertResult(id=str(result.inserted_id))
