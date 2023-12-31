"""Test config."""


def test_config(app):
    """Test flask config."""
    assert app.config.get("SQLALCHEMY_TRACK_MODIFICATIONS") is True
    assert app.config.get("FLASK_DEBUG") == 1
