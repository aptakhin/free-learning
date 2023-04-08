import logging
import logging.config  # noqa: WPS301
import random
import uuid
from unittest.mock import AsyncMock

import pytest
from app import create_app
from base.config import (FL_MODULE_BASE, FL_MODULE_BASE_ENTITY,
                         FL_MODULE_BASE_LINK_CHILD_OF,
                         FL_MODULE_BASE_LINK_NEXT_OF, FL_MODULE_BASE_WEB_ROUTE,
                         Settings)
from base.db import get_db
from base.db_age import Database
from base.email import Emailer
from base.models import Entity, Link
from container import container
from fastapi.testclient import TestClient
from httpx import Request, Response

logger = logging.getLogger(__name__)


@pytest.fixture()
def test_app():
    app = create_app()

    yield app


def log_request(request: Request):
    print(f'Send request: {request.method} {request.url}')
    print(f'...[headers]: {request.headers}')
    print(f'...   [body]: {request.content}')


def log_response(response: Response):
    print(f'Got response: {response} {response.url}')


@pytest.fixture()
def client(test_app):
    test_client = TestClient(test_app)

    test_client.event_hooks['request'] = [log_request]
    test_client.event_hooks['response'] = [log_response]

    yield test_client


@pytest.fixture()
def mock_db():
    container.register(Database, AsyncMock)
    return container.resolve(Database)


@pytest.fixture()
def mock_emailer():
    container.register(Emailer, AsyncMock)
    return container.resolve(Emailer)


@pytest.fixture()
def test_org():
    yield 'test_org'


@pytest.fixture()
def unsaved_entity():
    yield Entity(
        typ=FL_MODULE_BASE_ENTITY,
        subject_id=str(uuid.uuid4()),
    )


@pytest.fixture()
def saved_entity1(client, unsaved_entity):
    response1 = client.post(
        f'/api/{FL_MODULE_BASE}/v1/upsert-entity',
        json=unsaved_entity.dict(),
    )
    yield response1.json()


@pytest.fixture()
def saved_entity2(client, unsaved_entity):
    response2 = client.post(
        f'/api/{FL_MODULE_BASE}/v1/upsert-entity',
        json=unsaved_entity.dict(),
    )
    yield response2.json()


@pytest.fixture()
async def database_conn_iter():
    async for database_conn in get_db(Settings()):
        yield database_conn


def generate_lorem_ipsum(num_paragraphs=1, num_sentences=5):
    lorem_ipsum = []
    for _ in range(num_paragraphs):
        for _ in range(num_sentences):
            lorem_ipsum.append('Lorem ipsum dolor sit amet, ')
            lorem_ipsum.append('consectetur adipiscing elit. ')
        lorem_ipsum.append('\n\n')
    return ''.join(lorem_ipsum)


async def make_linked(db, *, num_link_to_root_entities: int):
    entity = Entity(
        typ=FL_MODULE_BASE_ENTITY,
        subject_id=str(uuid.uuid4()),
        properties={
            'title': generate_lorem_ipsum(num_paragraphs=1, num_sentences=1),
            'main': {
                'parser': {
                    'name': 'com.freelearning.base.markdown_parser',
                    'version': 1,
                },
                'content': generate_lorem_ipsum(
                    num_paragraphs=int(random.uniform(6, 10)),  # noqa: S311
                    num_sentences=int(random.uniform(6, 10)),  # noqa: S311
                ),
                'blocks': [],
            },
            'addon': {
                'blocks': [],
            },
        },
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

    for counter in range(num_link_to_root_entities):
        text = generate_lorem_ipsum(
            num_paragraphs=int(random.uniform(1, 5)),  # noqa: S311
            num_sentences=int(random.uniform(3, 10)),  # noqa: S311
        )

        if counter == 0:
            text = 'https://miro.com/app/board/uXjVP6is-xM=/' + '\n\n' + text

        entity2 = Entity(
            typ=FL_MODULE_BASE_ENTITY,
            subject_id=str(uuid.uuid4()),
            properties={
                'main': {
                    'content': text,
                    'parser': {
                        'name': 'com.freelearning.base.markdown_parser',
                        'version': 1,
                    },
                    'blocks': [],
                },
            },
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


@pytest.fixture()
async def db(database_conn):
    yield database_conn


base_logger_config = {
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
            'format': '{asctime} {levelname:8s} {name:15s} {message}',
            'datefmt': '%Y-%m-%d %H:%M:%S',  # noqa: WPS323
            'style': '{',
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
}


@pytest.fixture(scope='session', autouse=True)
def logger():
    logging.config.dictConfig(base_logger_config)
    yield


@pytest.fixture()
def debug_log(caplog):
    caplog.set_level(logging.DEBUG)
    yield
    caplog.set_level(logging.INFO)
