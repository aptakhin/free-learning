
from base.db_age import loads, dumps, make_properties


def test_load():
    assert loads('{"id": 281474976710709, "label": "", "properties": {"name": "Andres"}}::vertex') == {"id": 281474976710709, "label": "", "properties": {"name": "Andres"}}


def test_properties_make():
    assert make_properties({'a': 1}) == '{a: 1}'
    assert make_properties({'a': 1, 'b': 2}) == '{a: 1, b: 2}'
