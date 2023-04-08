import asyncio
from typing import Iterator

from base.config import Settings, get_settings
from base.db_age import Database
from fastapi import Depends
from container import container


def create_db_sync(settings: Settings):
    asyncio.get_event_loop().run_until_complete(
        Database.create_engine(settings.db_url),
    )


async def get_db() -> Iterator[Database]:
    """Retrieve db client."""
    yield container.resolve(Database)
