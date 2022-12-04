"""."""

import uuid

from base.models import Entity


def test_entity__upsert__insert(client, test_org):
    entity = Entity(
        id=str(uuid.uuid4()),
        subject_id=str(uuid.uuid4()),
    )
    add_json = entity.dict()
    response = client.post(
        f'/api/v1/base/{test_org}/upsert-entity',
        json=add_json,
    )
    assert response.status_code == 200, response.text

    js = response.json()
    assert js['id'], js
