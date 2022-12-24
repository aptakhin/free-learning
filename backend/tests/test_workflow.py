"""."""

import uuid

from base.models import Entity
from base.config import FL_MODULE_WORKDOMAIN


def test_workflow__upsert__insert(client):
    entity = Entity(
        typ='hello',
        id=str(uuid.uuid4()),
        subject_id=str(uuid.uuid4()),
    )
    response = client.post(
        f'/api/{FL_MODULE_WORKDOMAIN}/v1/link',
        json=entity.dict(),
    )
    assert response.status_code == 200, response.text

    js = response.json()
    print(js)
    assert js['id'], js
