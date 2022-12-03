"""."""

from fastapi import APIRouter

router = APIRouter(
    prefix='/items',
    tags=['items'],
    responses={404: {'description': 'Not found'}},
)


@router.get('/')
async def read_main():
    """."""
    return {'msg': 'Hello World'}
