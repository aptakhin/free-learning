"""."""

import uuid

from base.config import FL_MODULE_BASE
from base.models import Entity, Link


def test_entity__upsert__insert(client, test_org):
    entity = Entity(
        typ='com.freelearning.hello',
        fid=str(uuid.uuid4()),
        subject_id=str(uuid.uuid4()),
    )
    response = client.post(
        f'/api/{FL_MODULE_BASE}/v1/upsert-entity',
        json=entity.dict(),
    )
    assert response.status_code == 200, response.text

    js = response.json()
    assert js['id'], js


def test_link_upsert__insert(client, test_org):
    e1 = Entity(
        typ='com.freelearning.hello',
        fid=str(uuid.uuid4()),
        subject_id=str(uuid.uuid4()),
    )
    response1 = client.post(
        f'/api/{FL_MODULE_BASE}/v1/upsert-entity',
        json=e1.dict(),
    )
    e1id = response1.json()['id']

    e2 = Entity(
        typ='com.freelearning.hello',
        fid=str(uuid.uuid4()),
        subject_id=str(uuid.uuid4()),
    )
    response2 = client.post(
        f'/api/{FL_MODULE_BASE}/v1/upsert-entity',
        json=e2.dict(),
    )
    e2id = response2.json()['id']
    print(response2.text, response2.json())

    link = Link(
        typ='com.freelearning.child_of',
        id=str(uuid.uuid4()),
        start_id=e1.fid,
        end_id=e2.fid,
    )
    response = client.post(
        f'/api/{FL_MODULE_BASE}/v1/upsert-link',
        json=link.dict(),
    )
    assert response.status_code == 200, response.text

    js = response.json()
    assert js['id'], js
