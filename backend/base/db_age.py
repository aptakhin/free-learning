"""
Custom parsing of age Postgres types.

As standard python age had running problems.
"""

import json


def loads(expr: str):
    """Loads AGE type."""
    expr = expr.replace('::vertex', '')
    expr = expr.replace('::edge', '')
    return json.loads(expr)


def dumps(_: ...):
    """Dumps AGE type."""
    pass


def make_properties(obj: dict[str, ...]) -> str:
    """Makes properties."""
    properties_str = ', '.join(f'{k}: {repr(v)}' for k, v in obj.items())
    return r'{{0}}'.format(properties_str)


def make_label(obj: str) -> str:
    """Makes label."""
    return '`{0}`'.format(obj)
