"""
Custom parsing of age Postgres types.

As standard python age had running problems.
"""

import json
import logging

from base.db import Database
from base.models import Entity, Link
from sqlalchemy import event
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.sql import text


logger = logging.getLogger(__name__)


class ApacheAgeDatabase(Database):
    """."""

    def __init__(self, engine):
        """."""
        self._engine = engine
        self._prep_statement_counter = 0

    @classmethod
    async def create_engine(cls, dsn: str):
        engine = create_async_engine(dsn)

        @event.listens_for(engine.sync_engine, 'connect')
        def register_types(dbapi_connection, *args):  # noqa: WPS430
            dbapi_connection.run_async(
                lambda asyncpg_conn: asyncpg_conn.set_type_codec(
                    'agtype',
                    encoder=dumps,
                    decoder=loads,
                    schema='ag_catalog',
                ),
            )

        async with engine.begin() as conn:
            await conn.execute(text('CREATE EXTENSION IF NOT EXISTS age'))
            await conn.execute(text("LOAD 'age'"))
            await conn.execute(text(
                'SET search_path = ag_catalog, '
                '"$user", public',
            ))

        return ApacheAgeDatabase(engine)

    async def close(self):
        """Close connection."""
        await self._engine.dispose()

    async def upsert_entity(self, entity: Entity):
        label = make_label(entity.typ)
        properties = make_properties(entity.dict(exclude_none=True, exclude={'typ'}))
        query = f"""SELECT * FROM cypher('msft', $$
            CREATE (a :{label} {properties})
            RETURN a
        $$) as (a agtype);"""

        logger.debug('Insert link query')
        async with self._engine.begin() as conn:
            result = await conn.execute(text(query))
            result_row, = result.one()
        logger.debug('Insert link query result')
        return result_row

    async def upsert_link(self, link: Link):
        label = make_label(link.typ)
        properties = make_properties(link.dict(exclude_none=True, exclude={'typ', 'start_id', 'end_id'}))

        param_obj = {
            'link_start_id': link.start_id,
            'link_end_id': link.end_id,
            'label': label,
            'properties': properties,
        }
        param_obj_str = json.dumps(param_obj)
        logger.debug('Upsert link query result: %s', param_obj_str)
        prep_query = f"""
            PREPARE upsert_link_procedure_{self._prep_statement_counter}(agtype) AS
            SELECT * FROM cypher('msft', $$
            MATCH (a), (b)
            WHERE id(a) = $link_start_id AND id(b) = $link_end_id
            CREATE (a)-[e :{label} {properties}]->(b)
            RETURN e
        $$, $1) as (items agtype);"""
        logger.debug('Upsert link query')
        async with self._engine.begin() as conn:
            result = await conn.execute(text(prep_query))
            result = await conn.execute(text("EXECUTE upsert_link_procedure_{0}('{1}');".format(self._prep_statement_counter, param_obj_str)))
            result_row = result.scalar_one()

        self._prep_statement_counter += 1
        return result_row

    async def query_linked(self, query: str):
        query_id = int(query)
        prep_query = f"""
            PREPARE query_linked_procedure_{self._prep_statement_counter}(agtype) AS
            SELECT * FROM cypher('msft', $$
            MATCH (a:`com.freelearning.base.entity`)-[r:`com.freelearning.base.CHILD_OF`]-(b)
            WHERE id(a) = $query_id
            RETURN r
        $$, $1) as (items agtype);"""
        logger.debug('Insert link query')
        async with self._engine.begin() as conn:
            result = await conn.execute(text(prep_query))
            param_obj_str = json.dumps({'query_id': query_id})
            result = await conn.execute(text("EXECUTE query_linked_procedure_{0}('{1}')".format(self._prep_statement_counter, param_obj_str)))
            result_raw = result.all()
            result = [x[0] for x in result_raw]
        logger.debug('Insert link query result')
        self._prep_statement_counter += 1
        return result


def loads(expr: str):
    expr = expr.replace('::vertex', '')
    expr = expr.replace('::edge', '')
    return json.loads(expr)


def dumps(_: ...):
    pass


def make_properties(obj: dict[str, ...]) -> str:
    properties_str = ', '.join('{0}: {1}'.format(k, repr(v)) for k, v in obj.items())  # noqa: WPS111
    return '{{{0}}}'.format(properties_str)


def make_label(obj: str) -> str:
    return '`{0}`'.format(obj)
