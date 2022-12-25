"""."""

from base.db_age import loads, make_label, make_properties


def test_load():
    assert loads('{"id": 281474976710709, "label": "", "properties": {"name": "Andres"}}::vertex') == {'id': 281474976710709, 'label': '', 'properties': {'name': 'Andres'}}  # noqa: E501


def test_edge():
    assert loads('{"id": 1407374883553282, "label": "RELTYPE", "end_id": 1970324836974593, "start_id": 1970324836974594, "properties": {"name": null}}::edge') == {'id': 1407374883553282, 'label': 'RELTYPE', 'end_id': 1970324836974593, 'start_id': 1970324836974594, 'properties': {'name': None}}  # noqa: E501


def test_list():
    assert loads('[{"id": 3659174697238529, "label": "HELLO", "end_id": 3096224743817317, "start_id": 3096224743817316, "properties": {"fid": "74276499-5d6e-48c3-96b9-07672241c621", "subject_id": "2efd92fb-7c56-43e7-8e0e-655b13e4524f"}}::vertex]') == [{'id': 3659174697238529, 'label': 'HELLO', 'end_id': 3096224743817317, 'start_id': 3096224743817316, 'properties': {'fid': '74276499-5d6e-48c3-96b9-07672241c621', 'subject_id': '2efd92fb-7c56-43e7-8e0e-655b13e4524f'}}]  # noqa: E501


def test_properties_make():
    assert make_properties({'a': 1}) == '{a: 1}'
    assert make_properties({'a': 1, 'b': 2}) == '{a: 1, b: 2}'


def test_make_label():
    assert make_label('hello.world') == '`hello.world`'
