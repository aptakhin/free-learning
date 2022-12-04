"""."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app import create_app
from base.routes import router


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
