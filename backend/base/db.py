
from base.config import Settings, get_settings
from base.db_age import Database
from fastapi import Depends

# Database = ApacheAgeDatabase


async def get_db(settings: Settings = Depends(get_settings)) -> Database:  # noqa: B008
    """Retrieves db client."""
    database: Database = await Database.create_engine(settings.db_url)
    yield database
    await database.close()
