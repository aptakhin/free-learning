"""."""

# import asyncpg
from base.config import Settings, get_settings
# # from base.db_age import dumps as age_dumps, loads as age_loads
from fastapi import Depends
# from sqlalchemy import event
# from sqlalchemy.ext.asyncio import create_async_engine


class Database(object):
    pass


async def get_db(settings: Settings = Depends(get_settings)):  # noqa: B008
    """Retrieves db client."""
    from base.db_age import ApacheAgeDatabase

    database: Database = await ApacheAgeDatabase.create_engine(settings.db_url)

    yield database

    await database.close()
