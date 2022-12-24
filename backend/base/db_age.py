"""Custom parsing of age Postgres types as standard python age had
running problems."""
import json


def loads(expr: str):
    expr = expr.replace('::vertex', '')
    expr = expr.replace('::edge', '')
    return json.loads(expr)


def dumps(obj):
    ...


def make_properties(obj: dict[str, ...]) -> str:
    return '{' + ', '.join(f'{k}: {repr(v)}' for k, v in obj.items()) + '}'


def make_label(obj: str) -> str:
    return '`{}`'.format(obj)
