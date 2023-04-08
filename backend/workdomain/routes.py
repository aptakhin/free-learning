from base.db import get_db
from fastapi import APIRouter, Depends

router = APIRouter(
    prefix='/api/{FL_MODULE_WORKDOMAIN}/v1',
    tags=['workdomain'],
    responses={404: {'description': 'Not found'}},
)


@router.post('/link')
async def link(
    # entity: Entity,
    # org: str,
    db=Depends(get_db),
    # settings=Depends(get_settings),
):
    """Links entity."""
    # await upsert_entity(
    #     entity=Entity(subject_id='abc', id='bcde', type_='abc'),
    #     org=org,
    #     db=db,
    # )
    return {'id': 'hello'}
