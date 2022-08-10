import pytest

from spar import create_app, db
from spar.config import TestConfig


@pytest.fixture
def test_app():
    app = create_app(TestConfig)
    yield app


@pytest.fixture
def test_client(test_app):
    with test_app.app_context():
        test_client = test_app.test_client()
        yield test_client


@pytest.fixture
def test_db(test_app):
    with test_app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()