"""
Custom parsing of age Postgres types.

As standard python age had running problems.
"""

import json

import asyncpg
from base.config import Settings, get_settings
# from base.db_age import dumps as age_dumps, loads as age_loads
from fastapi import Depends
from sqlalchemy import event
from sqlalchemy.ext.asyncio import create_async_engine

from base.db import Database

class ApacheAgeDatabase(Database):
    def __init__(self, engine):
        self._engine = engine

    @staticmethod
    async def create_engine(dsn: str):
        engine = create_async_engine(
            dsn,
            echo=True,
        )

        async with engine.begin() as conn:
            from sqlalchemy.sql import text
            await conn.execute(text('CREATE EXTENSION IF NOT EXISTS age'))
            await conn.execute(text("LOAD 'age'"))
            await conn.execute(text('SET search_path = ag_catalog, "$user", public'))
            # await conn.execute(text("SELECT * FROM ag_catalog.drop_graph('msft', true)"))
            # await conn.execute(text("SELECT * FROM ag_catalog.create_graph('msft')"))

            # @event.listens_for(engine.sync_engine, 'connect')
            # def register_custom_types(dbapi_connection):
            #     print('Register comm')
            #     dbapi_connection.run_async(
            #         lambda connection: connection.set_type_codec(
            #             'agtype',
            #             encoder=age_dumps,
            #             decoder=age_loads,
            #             schema='ag_catalog',
            #         ),
            #     )
        return ApacheAgeDatabase(engine)

    async def close(self):
        await self._engine.dispose()


def loads(expr: str):
    """Loads AGE type."""
    print(expr, type(expr))
    expr = expr.replace('::vertex', '')
    expr = expr.replace('::edge', '')
    return json.loads(expr)


def dumps(_: ...):
    """Dumps AGE type."""
    pass


def make_properties(obj: dict[str, ...]) -> str:
    """Makes properties."""
    properties_str = ', '.join(f'{k}: {repr(v)}' for k, v in obj.items())
    return '{{{0}}}'.format(properties_str)


def make_label(obj: str) -> str:
    """Makes label."""
    return '`{0}`'.format(obj)
