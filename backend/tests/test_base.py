"""."""
import json
import logging
import pytest

from base.models import Entity, Link, EntityQuery
from base.config import FL_MODULE_BASE, FL_MODULE_BASE_LINK_CHILD_OF, FL_MODULE_BASE_WEB_ROUTE, FL_MODULE_BASE_LINK_NEXT_OF
from conftest import make_linked


def test_entity__upsert__insert(client, unsaved_entity: Entity):
    response = client.post(
        f'/api/{FL_MODULE_BASE}/v1/upsert-entity',
        json=unsaved_entity.dict(),
    )

    assert response.status_code == 200, response.text
    js = response.json()
    assert js['id'], js


def test_link_upsert__insert(client, saved_entity1: dict, saved_entity2: dict):
    link = Link(
        typ=FL_MODULE_BASE_LINK_CHILD_OF,
        start_id=saved_entity1['id'],
        end_id=saved_entity2['id'],
        text='',
    )

    response = client.post(
        f'/api/{FL_MODULE_BASE}/v1/upsert-link',
        json=link.dict(),
    )

    assert response.status_code == 200, response.text
    js = response.json()
    assert js['id'], js


@pytest.mark.asyncio
async def test_query(client, database_conn_iter):
    async for database_conn in database_conn_iter:
        root_entity = await make_linked(database_conn)

    query = EntityQuery(
        end_entity_id=int(root_entity['id']),
        # from_entity_label=FL_MODULE_BASE_WEB_ROUTE,
        link_label=FL_MODULE_BASE_LINK_CHILD_OF,
    )
    # print('z', query.dict())
    # logger.debug('Query args: %s', query.dict()))
    response = client.get(
        f'/api/{FL_MODULE_BASE}/v1/query-linked/',
        params=query.dict(exclude_none=True),
    )

    assert response.status_code == 200, response.text
    js = response.json()
    # logger.debug('Got response: %s', json.dumps(js, indent=3))
    assert js['result'][0][0]['id'], js


# @pytest.mark.skip
@pytest.mark.asyncio
async def test_query__start_properties(client, database_conn_iter, debug_log):
    async for database_conn in database_conn_iter:
        root_entity = await make_linked(database_conn)

        route_results = await database_conn.query_linked(
            start_entity_label=FL_MODULE_BASE_WEB_ROUTE,
            start_entity_properties={'route': 'web/test'},
            link_label=FL_MODULE_BASE_LINK_NEXT_OF,
            end_entity_id=int(root_entity['id']),
        )

        assert len(route_results) == 1
