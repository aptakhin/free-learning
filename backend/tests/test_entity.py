
import uuid
from fl_core.models import Entity


def test_item_insert(client, test_org):
    entity = Entity(id=str(uuid.uuid4()), subject_id=str(uuid.uuid4()))
    response = client.post(f'/api/v1/{test_org}/upsert-entity', json=entity.json())
    assert response.status_code == 200
    assert response.json() == {"status": True}
