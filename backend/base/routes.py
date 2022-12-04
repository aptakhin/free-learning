"""."""

from fastapi import APIRouter, Depends
import motor.motor_asyncio
from base.models import Entity, EntityUpsertResult
from base.config import Settings

router = APIRouter(
    prefix='/api/v1/base',
    tags=['base'],
    responses={404: {'description': 'Not found'}},
)


def get_settings():
    return Settings()


async def get_db(settings: Settings = Depends(get_settings)):
    """Retrieves db client."""
    client = motor.motor_asyncio.AsyncIOMotorClient(
        host=settings.mongodb_url,
    )

    yield client.test

    client.close()


@router.post('/{org}/upsert-entity', response_model=EntityUpsertResult)
async def upsert_entity(
    entity: Entity,
    org: str,
    db=Depends(get_db),  # noqa: B008
):
    """Upserts entity."""
    result = await db.entities.insert_one(entity.insert_dict())
    return EntityUpsertResult(id=str(result.inserted_id))
