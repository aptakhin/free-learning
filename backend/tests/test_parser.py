import copy
from base.config import FL_MODULE_BASE_ENTITY
from base.models import Entity
from base.view import prepare_view_inplace


def test_parser():
    entity = Entity(
        typ=FL_MODULE_BASE_ENTITY,
        properties={
            'main': {
                'content': 'hello https://miro.com/app/board/uXjVP6is-xM=/ and buy',
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
    assert len(result['properties']['main']['blocks']['items']) == 3
    items = result['properties']['main']['blocks']['items']
    assert items[0]['typ'] == 'com.freelearning.base.markdown_html'
    assert items[0]['content'] == '<p>hello</p>\n'
    assert items[1]['typ'] == 'com.freelearning.miro.block'
    assert items[2]['typ'] == 'com.freelearning.base.markdown_html'
