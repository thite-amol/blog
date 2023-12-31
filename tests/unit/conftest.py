"""Fixture module."""
import pytest

from src.app import create_app


@pytest.fixture
def app():
    """Create default app object."""
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
        }
    )

    return app


@pytest.fixture
def client(app):
    """Create an app testing client."""
    with app.test_client() as client:
        yield client
