"""Flask App configuration."""
from os import environ


class Config:
    """Set Flask config variables."""

    # General Config
    ENVIRONMENT = environ.get("ENVIRONMENT", "development")
    FLASK_DEBUG = environ.get("FLASK_DEBUG", 1)
    SECRET_KEY = environ.get("SECRET_KEY", "3d6f45a5fc12445dbac2f59c3b6c7cb1")
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"

    # Database
    """
    # SQLite, relative to Flask instance path
    sqlite:///project.db

    # PostgreSQL
    postgresql://scott:tiger@localhost/project

    # MySQL / MariaDB
    mysql://scott:tiger@localhost/project
    """

    SQL_DATABASE_URI = "sqlite:///blog.db"
    SQLALCHEMY_DATABASE_URI = environ.get(
        "SQLALCHEMY_DATABASE_URI", SQL_DATABASE_URI
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = True
