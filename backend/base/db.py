"""."""

from base.config import Settings, get_settings
from fastapi import Depends


class Database(object):
    pass


async def get_db(settings: Settings = Depends(get_settings)) -> 'ApacheAgeDatabase':  # noqa: B008
    """Retrieves db client."""
    from base.db_age import ApacheAgeDatabase

    database: Database = await ApacheAgeDatabase.create_engine(settings.db_url)

    yield database

    await database.close()
