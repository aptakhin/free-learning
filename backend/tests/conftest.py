"""."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fl_core.routes import router


@pytest.fixture
def test_app():
    app = FastAPI()
    app.include_router(router)
    yield app


@pytest.fixture
def client(test_app):
    cl = TestClient(test_app)
    yield cl


@pytest.fixture
def test_org():
    yield 'test_org'
