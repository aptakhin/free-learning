"""."""

import uuid

from base.config import FL_MODULE_BASE, FL_MODULE_BASE_LINK_CHILD_OF
from base.models import Entity, Link


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
    )

    response = client.post(
        f'/api/{FL_MODULE_BASE}/v1/upsert-link',
        json=link.dict(),
    )

    assert response.status_code == 200, response.text
    js = response.json()
    assert js['id'], js
