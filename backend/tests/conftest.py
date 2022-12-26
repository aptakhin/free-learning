"""."""

import logging
import logging.config
import uuid

from app import create_app
from base.config import FL_MODULE_BASE, FL_MODULE_BASE_ENTITY, Settings, FL_MODULE_BASE_LINK_CHILD_OF
from base.db import get_db
from base.models import Entity, Link
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import event


logger = logging.getLogger(__name__)


@pytest.fixture
def test_app():
    app = create_app()
    yield app


@pytest.fixture
def client(test_app):
    cl = TestClient(test_app)
    yield cl


@pytest.fixture
def test_org():
    yield 'test_org'


@pytest.fixture
def unsaved_entity():
    yield Entity(
        typ=FL_MODULE_BASE_ENTITY,
        subject_id=str(uuid.uuid4()),
    )


@pytest.fixture
def saved_entity1(client, unsaved_entity):
    response1 = client.post(
        f'/api/{FL_MODULE_BASE}/v1/upsert-entity',
        json=unsaved_entity.dict(),
    )
    yield response1.json()


@pytest.fixture
def saved_entity2(client, unsaved_entity):
    response2 = client.post(
        f'/api/{FL_MODULE_BASE}/v1/upsert-entity',
        json=unsaved_entity.dict(),
    )
    yield response2.json()


@pytest.fixture
async def database_conn_iter():
    async for database_conn in get_db(Settings()):
        yield database_conn


async def make_linked(db):
    entity = Entity(
        typ=FL_MODULE_BASE_ENTITY,
        subject_id=str(uuid.uuid4()),
    )
    entity_row = await db.upsert_entity(entity)

    for _ in range(10):
        entity2 = Entity(
            typ=FL_MODULE_BASE_ENTITY,
            subject_id=str(uuid.uuid4()),
        )
        entity2_row = await db.upsert_entity(entity2)

        link = Link(
            typ=FL_MODULE_BASE_LINK_CHILD_OF,
            start_id=entity2_row['id'],
            end_id=entity_row['id'],
            text='',
        )
        await db.upsert_link(link)

    return entity_row


@pytest.fixture(scope='function')
async def db(database_conn):
    yield database_conn

@pytest.fixture(scope='session', autouse=True)
def logger():
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': True,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'level': 'INFO',
                'stream': 'ext://sys.stdout',
            },
        },
        'formatters': {
            'default': {
                'format': '%(asctime)s %(levelname)-8s %(name)-15s %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
        },
        'loggers': {
            'root': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
            'base': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
            'sqlalchemy.engine': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
        },
    })
    yield


# @pytest.fixture(scope='function', autouse=False)
# async def db(database_conn):
#     """
#     SQLAlchemy session started with SAVEPOINT.

#     After test rollback to this SAVEPOINT.
#     """
    # # begin a non-ORM transaction
    # trans = await database_conn.begin()
    # session = sessionmaker()(bind=database_conn)

    # session.begin_nested()  # SAVEPOINT
    # logger.debug('begin_nested')


    # # await trans.execute(text('dd'))
    # # await conn.execute(text("SELECT * FROM ag_catalog.drop_graph('msft', true)"))
    # # await conn.execute(text("SELECT * FROM ag_catalog.create_graph('msft')"))

    # @event.listens_for(session, 'after_transaction_end')
    # def restart_savepoint(session, transaction):
    #     """Each time that SAVEPOINT ends, reopen it."""
    #     logger.debug('restart_savepoint')
    #     if transaction.nested and not transaction._parent.nested:
    #         session.begin_nested()

    # yield session

    # logger.debug('Close session')
    # session.close()
    # trans.rollback()  # roll back to the SAVEPOINT
