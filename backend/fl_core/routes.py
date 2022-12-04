"""."""

from fastapi import APIRouter, Depends
import motor.motor_asyncio
import fl_core.config as config

router = APIRouter(
    prefix='/api/v1',
    tags=['base'],
    responses={404: {'description': 'Not found'}},
)


async def get_db():
    print(config.MONGODB_URL)
    client = motor.motor_asyncio.AsyncIOMotorClient(host=config.MONGODB_URL, serverSelectionTimeoutMS=50, connect=False)
    try:
        print(await client.server_info())
    except Exception:
        print("Unable to connect to the server.")

    try:
        yield client
    finally:
        client.close()



@router.get('/healthz')
async def healthz():
    """."""
    return {'status': True}


@router.post('/{org}/upsert-entity')
async def upsert_entity(org, db=Depends(get_db)):
    """."""
    await db.test.collection.insert_one({'test': 1})
    return {'status': True}
