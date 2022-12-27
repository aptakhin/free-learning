"""
Custom parsing of age Postgres types.

As standard python age had running problems.
"""

import json
import logging
from typing import Optional

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
        prepared_dict = entity.dict(exclude_none=True, exclude={'typ', 'properties'})
        prepared_dict.update(entity.properties)
        properties = make_properties(prepared_dict)
        query = f"""SELECT * FROM cypher('msft', $$
            CREATE (a {label} {properties})
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
            CREATE (a)-[e {label} {properties}]->(b)
            RETURN e
        $$, $1) as (items agtype);"""
        logger.debug('Upsert link query')
        async with self._engine.begin() as conn:
            result = await conn.execute(text(prep_query))
            result = await conn.execute(text("EXECUTE upsert_link_procedure_{0}('{1}');".format(self._prep_statement_counter, param_obj_str)))
            result_row = result.scalar_one()

        self._prep_statement_counter += 1
        return result_row

    async def query_linked(
        self,
        start_entity_id: Optional[int] = None,
        start_entity_label: Optional[str] = None,
        start_entity_properties: Optional[dict] = None,
        link_label: Optional[str] = None,
        link_properties: Optional[dict] = None,
        end_entity_id: Optional[int] = None,
        end_entity_label: Optional[str] = None,
        end_entity_properties: Optional[dict] = None,
    ):
        cond = []
        params = {}

        if start_entity_id:
            cond.append('id(a) = $start_entity_id')
            params['start_entity_id'] = start_entity_id
        if end_entity_id:
            if cond:
                cond.append('AND')
            cond.append('id(b) = $end_entity_id')
            params['end_entity_id'] = end_entity_id

        where_cond = ''
        if cond:
            where_cond = 'WHERE ' + ' '.join(cond)

#         prep_query = f"""
#             PREPARE query_linked_procedure_{self._prep_statement_counter}(agtype) AS
#             SELECT * FROM cypher('msft', $$
#             MATCH (director)-[r:`com.freelearning.base.NEXT_OF`]->(movie)
# RETURN movie
#         $$, $1) as (items agtype);"""

        prep_query = f"""
            PREPARE query_linked_procedure_{self._prep_statement_counter}(agtype) AS
            SELECT * FROM cypher('msft', $$
            MATCH (a{make_label(start_entity_label)} {make_properties(start_entity_properties)})-[r{make_label(link_label)} {make_properties(link_properties)}]->(b{make_label(end_entity_label)} {make_properties(end_entity_properties)})
            {where_cond}
            RETURN [a, r, b]
        $$, $1) as (items agtype);"""
        logger.debug('Insert link query')
        async with self._engine.begin() as conn:
            result = await conn.execute(text(prep_query))
            param_obj_str = json.dumps(params)
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


def make_properties(obj: Optional[dict[str, ...]]) -> str:
    if obj is None:
        return ''
    properties_str = ', '.join('{0}: {1}'.format(k, repr(v)) for k, v in obj.items())  # noqa: WPS111
    return '{{{0}}}'.format(properties_str)


def make_label(obj: Optional[str]) -> str:
    return ':`{0}`'.format(obj) if obj is not None else ''
