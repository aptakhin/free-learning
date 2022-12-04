"""."""

from fastapi import APIRouter, Depends
import motor.motor_asyncio
from fl_core.models import Entity
import fl_core.config as config

router = APIRouter(
    prefix='/api/v1',
    tags=['base'],
    responses={404: {'description': 'Not found'}},
)


async def get_db():
    """Retrieves db client."""
    client = motor.motor_asyncio.AsyncIOMotorClient(
        host=config.MONGODB_URL,
        connect=False,
    )

    yield client.test

    client.close()


@router.get('/healthz')
async def healthz():
    """."""
    return {'status': True}


@router.post('/{org}/upsert-entity')
async def upsert_entity(entity: Entity, org: str, db=Depends(get_db)):  # noqa: B008
    """Upserts entity."""
    result = await db.entities.insert_one(entity.json())
    return {'status': result}
