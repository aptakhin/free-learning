"""."""

import uuid

from base.config import FL_MODULE_BASE
from base.models import Entity


def test_entity__upsert__insert(client, test_org):
    entity = Entity(
        typ='hello',
        id=str(uuid.uuid4()),
        subject_id=str(uuid.uuid4()),
    )
    add_json = entity.dict()
    response = client.post(
        f'/api/{FL_MODULE_BASE}/v1/upsert-entity',
        json=add_json,
    )
    assert response.status_code == 200, response.text

    js = response.json()
    assert js['id'], js
