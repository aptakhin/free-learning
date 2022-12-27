"""."""

import logging.config  # noqa: WPS301
import random
import uuid

from app import create_app
from base.config import (
    FL_MODULE_BASE, FL_MODULE_BASE_ENTITY,
    Settings, FL_MODULE_BASE_LINK_CHILD_OF,
    FL_MODULE_BASE_WEB_ROUTE, FL_MODULE_BASE_LINK_NEXT_OF,
)
from base.db import get_db
from base.models import Entity, Link
from fastapi.testclient import TestClient
import pytest


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


def generate_lorem_ipsum(num_paragraphs=1, num_sentences=5):
    lorem_ipsum = ""
    for i in range(num_paragraphs):
        for j in range(num_sentences):
            lorem_ipsum += "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
        lorem_ipsum += "\n\n"
    return lorem_ipsum


async def make_linked(db):
    entity = Entity(
        typ=FL_MODULE_BASE_ENTITY,
        subject_id=str(uuid.uuid4()),
        properties={},
    )
    entity_row = await db.upsert_entity(entity)

    web_route = Entity(
        typ=FL_MODULE_BASE_WEB_ROUTE,
        properties={
            'route': 'web/test',
        },
    )
    web_route_row = await db.upsert_entity(web_route)
    link = Link(
        typ=FL_MODULE_BASE_LINK_NEXT_OF,
        start_id=web_route_row['id'],
        end_id=entity_row['id'],
        text='',
    )
    await db.upsert_link(link)

    for _ in range(10):
        entity2 = Entity(
            typ=FL_MODULE_BASE_ENTITY,
            subject_id=str(uuid.uuid4()),
            properties={
                'text': generate_lorem_ipsum(num_paragraphs=int(random.uniform(1, 5)), num_sentences=int(random.uniform(3, 10)))
            }
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
                'format': '%(asctime)s %(levelname)-8s '
                '%(name)-15s %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',  # noqa: WPS323
            },
        },
        'loggers': {
            'root': {
                'handlers': ['console'],
                'level': 'ERROR',
            },
            'base': {
                'handlers': ['console'],
                'level': 'ERROR',
            },
            'sqlalchemy.engine': {
                'handlers': ['console'],
                'level': 'ERROR',
            },
        },
    })
    yield


@pytest.fixture(scope='function')
def debug_log(caplog):
    caplog.set_level(logging.DEBUG)

    # yield
