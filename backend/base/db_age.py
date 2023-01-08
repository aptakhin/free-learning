"""
Custom parsing of age Postgres types.

As standard python age had running problems.
"""

import json
import logging
from typing import Any, Optional

from base.models import Account, AccountA14N
from base.db_tables import account, account_a14n_provider, account_a14n_signature
from base.models import Entity, Link, EntityQuery
from sqlalchemy import event, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.sql import text


logger = logging.getLogger(__name__)


class Database(object):
    """."""

    def __init__(self, engine):
        """."""
        self._engine = engine
        self._prep_statement_counter = 0

    @classmethod
    async def create_engine(cls, dsn: str):
        engine = create_async_engine(
            dsn,
            connect_args={'timeout': 5},
        )

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

        return Database(engine)

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

        logger.debug('Insert link query: {0}'.format(query))
        async with self._engine.begin() as conn:
            result = await conn.execute(text(query))
            result_row, = result.one()
        logger.debug('Insert link query result: {0}'.format(result_row))
        return result_row

    async def upsert_link(self, link: Link):
        label = make_label(link.typ)
        properties = make_properties(link.dict(exclude_none=True, exclude={'typ', 'start_id', 'end_id'}))

        param_obj = {
            'link_start_id': link.start_id,
            'link_end_id': link.end_id,
        }
        param_obj_str = json.dumps(param_obj)
        logger.debug('Upsert link query result: {0}'.format(param_obj_str))
        prep_query = f"""
            PREPARE upsert_link_procedure_{self._prep_statement_counter}(agtype) AS
            SELECT * FROM cypher('msft', $$
            MATCH (a), (b)
            WHERE id(a) = $link_start_id AND id(b) = $link_end_id
            CREATE (a)-[e {label} {properties}]->(b)
            RETURN e
        $$, $1) as (items agtype);"""
        logger.debug('Upsert link query: {0}'.format(prep_query))
        async with self._engine.begin() as conn:
            result = await conn.execute(text(prep_query))
            result = await conn.execute(text("EXECUTE upsert_link_procedure_{0}('{1}');".format(self._prep_statement_counter, param_obj_str)))
            result_row = result.scalar_one()

        logger.debug('Upsert link result: {0}'.format(result_row))
        self._prep_statement_counter += 1
        return result_row

    async def query_linked(
        self,
        q: EntityQuery,
    ):
        cond = []
        params = {}
        if q.start_entity_id:
            cond.append('id(a) = $start_entity_id')
            params['start_entity_id'] = int(q.start_entity_id)
        if q.end_entity_id:
            if cond:
                cond.append('AND')
            cond.append('id(b) = $end_entity_id')
            params['end_entity_id'] = int(q.end_entity_id)
        where_cond = ''
        if cond:
            where_cond = 'WHERE ' + ' '.join(cond)

        prep_query = f"""
            PREPARE query_linked_procedure_{self._prep_statement_counter}(agtype) AS
            SELECT * FROM cypher('msft', $$
            MATCH (a{make_label(q.start_entity_label)} {make_properties(q.start_entity_properties)})-[r{make_label(q.link_label)} {make_properties(q.link_properties)}]->(b{make_label(q.end_entity_label)} {make_properties(q.end_entity_properties)})
            {where_cond}
            RETURN [a, r, b]
        $$, $1) as (items agtype);"""
        param_obj_str = json.dumps(params)
        logger.debug('Get linked query: %s', prep_query)
        logger.debug('    params: %s', param_obj_str)
        async with self._engine.begin() as conn:
            await conn.execute(text(prep_query))
            statement_exec_result = await conn.execute(text("EXECUTE query_linked_procedure_{0}('{1}')".format(self._prep_statement_counter, param_obj_str)))
            query_result = [row.items for row in statement_exec_result]
        logger.debug('Linked query result: {0}'.format(json.dumps(query_result, indent=0)))
        self._prep_statement_counter += 1
        return query_result

    async def query_account_by_a14n_signature_type_and_value(self, *, signature_type: str, signature_value: str) -> AccountA14N:
        async with self._engine.begin() as conn:
            query = (
                select([
                    account.c.id.label('account_id'),
                    account_a14n_provider.c.id.label('account_a14n_provider_id'),
                    account_a14n_signature.c.id.label('account_a14n_signature_id'),
                ])
                .select_from(
                    account
                    .join(account_a14n_provider)
                    .join(account_a14n_signature),
                )
                .where(
                    account_a14n_signature.c.account_a14n_provider_type == signature_type,
                    account_a14n_signature.c.value == signature_value,
                )
            )
            query_response = await conn.execute(query)
            query_result = query_response.one_or_none()

            return AccountA14N(
                account_id=query_result['account_id'],
                account_a14n_provider_id=query_result['account_a14n_provider_id'],
                account_a14n_signature_id=query_result['account_a14n_signature_id'],
            ) if query_result else None

    async def add_account_new_a14n_signature(self, *, account_id: Optional[str], signature_type: str, signature_value: str) -> Optional[Account]:
        async with self._engine.begin() as conn:
            upsert_provider_query = (
                insert(account_a14n_provider)
                .values(
                    account_id=account_id,
                    type=signature_type,
                    value=signature_value,
                )
                .on_conflict_do_nothing(
                    index_elements=['account_id', 'type', 'value'],
                )
                .returning(
                    account_a14n_provider.c.id,
                    account_a14n_provider.c.type,
                )
            )
            provider_response = await conn.execute(upsert_provider_query)
            provider_result = provider_response.one()

            insert_signature_query = (
                insert(account_a14n_signature)
                .values(
                    account_a14n_provider_id=provider_result['id'],
                    account_a14n_provider_type=provider_result['type'],
                    value=signature_value,
                )
                .returning(
                    account_a14n_signature.c.id,
                )
            )
            insert_signature_response = await conn.execute(insert_signature_query)
            insert_signature_result = insert_signature_response.one()
            return Account(
                account_id=insert_signature_result['id'],
            )

    async def query_account_by_a14n_provider_type_and_value(
        self,
        provider_type: str,
        provider_value: str,
    ) -> Optional[dict]:
        async with self._engine.begin() as conn:
            query = (
                select(
                    account.c.id.label('account_id'),
                    account_a14n_provider.c.id.label('account_provider_id'),
                )
                .select_from(
                    account
                    .join(account_a14n_provider),
                )
                .where(
                    account_a14n_provider.c.type == provider_type,
                    account_a14n_provider.c.value == provider_value,
                )
            )
            query_response = await conn.execute(query)
            query_result = query_response.one_or_none()
            return dict(
                account_id=query_result['account_id'],
            ) if query_result else None

    async def add_new_account(self) -> Account:
        async with self._engine.begin() as conn:
            insert_account_query = (
                insert(account)
                .values()
                .returning(
                    account.c.id,
                )
            )
            insert_account_response = await conn.execute(insert_account_query)
            insert_account_result = insert_account_response.one()
            return Account(
                account_id=insert_account_result['account_id'],
            )

    async def move_a14n_provider_to_account(
        self,
        *,
        account_a14n_provider_id: str,
        account_id: str,
    ) -> None:
        async with self._engine.begin() as conn:
            update_provider_query = (
                account_a14n_provider.update()
                .where(account_a14n_provider.c.id == account_a14n_provider_id)
                .values(
                    account_id=account_id,
                )
            )
            await conn.execute(update_provider_query)


    async def confirm_a14n_with_device(self, account_a14n_signature_id: str, device: dict[str, Any]) -> None:
        async with self._engine.begin() as conn:
            update_provider_query = (
                account_a14n_signature.update()
                .where(account_a14n_signature.c.id == account_a14n_signature_id)
                .values(
                    device=device,
                )
            )
            await conn.execute(update_provider_query)


def loads(expr: str):
    expr = expr.replace('::vertex', '')
    expr = expr.replace('::edge', '')
    return json.loads(expr)


def dumps(_: Any):
    raise ValueError('Not implemented!')


def make_properties(obj: Optional[dict[str, Any]]) -> str:
    if obj is None:
        return ''
    elif isinstance(obj, (str, int)):
        return repr(obj)
    elif isinstance(obj, dict):
        properties_str = ', '.join('{0}: {1}'.format(k, make_properties(v)) for k, v in obj.items())  # noqa: WPS111
        return '{{{0}}}'.format(properties_str)
    elif isinstance(obj, list):
        properties_str = ', '.join(make_properties(v) for v in obj)  # noqa: WPS111
        return '{{{0}}}'.format(properties_str)
    else:
        raise ValueError('Unsupported type `{0}` for `make_properties`!'.format(type(obj)))


def make_label(obj: Optional[str]) -> str:
    return ':`{0}`'.format(obj) if obj is not None else ''
