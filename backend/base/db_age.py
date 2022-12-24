"""Custom parsing of age Postgres types as standard python age had
running problems."""
import json


def loads(expr: str):
    if expr.endswith('::vertex'):
        expr = expr.removesuffix('::vertex')
    return json.loads(expr)

def dumps(obj):
    ...

def make_properties(obj: dict[str, ...]) -> str:
    return '{' + ', '.join(f'{k}: {repr(v)}' for k, v in obj.items()) + '}'
