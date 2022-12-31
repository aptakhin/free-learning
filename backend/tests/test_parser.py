

import copy
from base.config import FL_MODULE_BASE_ENTITY
from base.models import Entity
from base.view import prepare_view_inplace


def test_parser():
    entity = Entity(
        typ=FL_MODULE_BASE_ENTITY,
        properties={
            'main': {
                'content': 'hello',
                'parser': {
                    'name': 'com.freelearning.base.markdown_parser',
                    'version': 1,
                },
                'blocks': [],
            },
        },
    )

    orig = copy.deepcopy(entity.dict())
    result = prepare_view_inplace(entity.dict())
    assert len(result['properties']['main']['blocks']) == 1
