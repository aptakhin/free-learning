"""."""

from fastapi import APIRouter, Depends
from httpx import AsyncClient
from base.config import get_settings, FL_MODULE_WORKDOMAIN
from base.db import get_db

# from app import get_app
from base.models import Entity, EntityUpsertResult
from base.routes import upsert_entity

router = APIRouter(
    prefix='/api/{FL_MODULE_WORKDOMAIN}/v1',
    tags=['workdomain'],
    responses={404: {'description': 'Not found'}},
)


@router.post('/link')
async def link(
    # entity: Entity,
    # org: str,
    db=Depends(get_db),  # noqa: B008
    # settings=Depends(get_settings),  # noqa: B008
):
    """Links entity."""
    # await upsert_entity(
    #     entity=Entity(subject_id='abc', id='bcde', type_='abc'),
    #     org=org,
    #     db=db,
    # )
    return {'id': 'hello'}
