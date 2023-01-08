"""."""
from base.models import Entity, Link, EntityQuery
from base.config import (
    FL_MODULE_BASE, FL_MODULE_BASE_LINK_CHILD_OF,
    FL_MODULE_BASE_WEB_ROUTE, FL_MODULE_BASE_LINK_NEXT_OF,
)
from conftest import make_linked
import pytest


@pytest.mark.move2acceptance
@pytest.mark.skip
def test_entity__upsert__insert(client, unsaved_entity: Entity):
    response = client.post(
        f'/api/{FL_MODULE_BASE}/v1/upsert-entity',
        json=unsaved_entity.dict(),
    )

    assert response.status_code == 200, response.text
    js = response.json()
    assert js['id'], js


@pytest.mark.move2acceptance
@pytest.mark.skip
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
@pytest.mark.move2acceptance
@pytest.mark.skip
async def test_query__end_entity_id(client, database_conn_iter):
    num_link_to_root_entities = 10

    async for database_conn in database_conn_iter:
        root_entity = await make_linked(
            database_conn,
            num_link_to_root_entities=num_link_to_root_entities,
        )

    with open('dump.txt', 'wt') as f:
        f.write(str(root_entity['id']))

    query = EntityQuery(
        link_label=FL_MODULE_BASE_LINK_CHILD_OF,
        end_entity_id=str(root_entity['id']),
    )
    # logger.debug('Query args: %s', query.dict()))
    response = client.post(
        f'/api/{FL_MODULE_BASE}/v1/query-linked/',
        json=query.dict(exclude_none=True),
    )

    assert response.status_code == 200, response.text
    js = response.json()
    assert js['query_result'], js
    assert js['query_result'][0], js['query_result']
    assert len(js['query_result']) == num_link_to_root_entities


@pytest.mark.asyncio
@pytest.mark.move2acceptance
@pytest.mark.skip
async def test_query__start_entity_label_and_properties(
    database_conn_iter,
    # debug_log,
):
    num_link_to_root_entities = 1
    async for database_conn in database_conn_iter:
        root_entity = await make_linked(
            database_conn,
            num_link_to_root_entities=num_link_to_root_entities,
        )

        route_results = await database_conn.query_linked(EntityQuery(
            start_entity_label=FL_MODULE_BASE_WEB_ROUTE,
            start_entity_properties={'route': 'web/test'},
            link_label=FL_MODULE_BASE_LINK_NEXT_OF,
            end_entity_id=str(root_entity['id']),
        ))

        assert len(route_results) == 1
