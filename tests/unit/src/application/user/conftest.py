"""Fixture module."""
import pytest

from src.application.user.model import User


@pytest.fixture
def user_detail():
    """Create user object with details."""
    return User(
        id=1,
        username="test_username",
        email="test@test.com",
        password="$2a$12$Whz9Bu5Y4h85hb5UST14N.UT1XRSuWqOJAPsOIEEf.BYleB0mWFoK",
        modified_at=None,
    )
