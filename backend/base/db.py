"""."""

import asyncpg
from fastapi import Depends
from base.db_age import loads as age_loads, dumps as age_dumps
from base.config import Settings, get_settings


async def get_db(settings: Settings = Depends(get_settings)):
    """Retrieves db client."""

    conn = await asyncpg.connect(settings.db_url)

    await conn.execute('CREATE EXTENSION IF NOT EXISTS age')
    await conn.execute("LOAD 'age'")
    await conn.execute('SET search_path = ag_catalog, "$user", public')

    await conn.set_type_codec(
        'agtype',
        encoder=age_dumps,
        decoder=age_loads,
        schema='ag_catalog',
    )

    yield conn

    await conn.close()
