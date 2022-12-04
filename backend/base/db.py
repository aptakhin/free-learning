from fastapi import APIRouter, Depends
import motor.motor_asyncio
from base.models import Entity, EntityUpsertResult
from base.config import Settings, get_settings


async def get_db(settings: Settings = Depends(get_settings)):
    """Retrieves db client."""
    client = motor.motor_asyncio.AsyncIOMotorClient(
        host=settings.mongodb_url,
        connect=False,
    )
    print('conn', settings.mongodb_url)
    yield client.test

    client.close()
