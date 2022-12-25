"""."""

import asyncpg
from base.config import Settings, get_settings
from base.db_age import dumps as age_dumps, loads as age_loads
from fastapi import Depends
from sqlalchemy import event
from sqlalchemy.ext.asyncio import create_async_engine


class Database(object):
    pass

class ApacheAgeDatabase(Database):
    def __init__(self):
        self._engine = None

    @staticmethod
    async def create_engine(cls, dsn: str):
        engine = create_async_engine(
            dsn,
            echo=True,
        )

        async with engine.begin() as conn:
            await conn.execute('CREATE EXTENSION IF NOT EXISTS age')
            await conn.execute("LOAD 'age'")
            await conn.execute('SET search_path = ag_catalog, "$user", public')

            @event.listens_for(engine.sync_engine, "connect")
            def register_custom_types(dbapi_connection, ...):
                dbapi_connection.run_async(
                    lambda connection: connection.set_type_codec(
                        'agtype',
                        encoder=age_dumps,
                        decoder=age_loads,
                        schema='ag_catalog',
                    )
                )

    async def close():
        await self._engine.dispose()


async def get_db(settings: Settings = Depends(get_settings)):  # noqa: B008
    """Retrieves db client."""

    database: Database = ApacheAgeDatabase.create_engine(settings.db_url)

    yield database

    await database.close()
