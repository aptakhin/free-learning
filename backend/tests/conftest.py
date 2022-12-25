"""."""

import uuid

import pytest
from fastapi.testclient import TestClient
from app import create_app
from base.config import FL_MODULE_BASE, FL_MODULE_BASE_ENTITY, Settings
from base.db import get_db
from base.models import Entity


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
async def database_conn():
    yield get_db(Settings())


@pytest.fixture(
    scope='function',
    autouse=True,
)
async def db(database_conn):
    """
    SQLAlchemy session started with SAVEPOINT.

    After test rollback to this SAVEPOINT.
    """
    # begin a non-ORM transaction
    trans = await database_conn.begin()
    session = sessionmaker()(bind=database_conn)

    session.begin_nested()  # SAVEPOINT

    # app.tests.config.session = session  # Inject session to the server code under test

    @event.listens_for(session, 'after_transaction_end')
    def restart_savepoint(session, transaction):
        """Each time that SAVEPOINT ends, reopen it."""
        if transaction.nested and not transaction._parent.nested:
            session.begin_nested()

    yield session

    session.close()
    trans.rollback()  # roll back to the SAVEPOINT
