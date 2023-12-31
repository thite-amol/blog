"""This module is used to automated deployment related stuff."""
from flask_migrate import migrate, upgrade

from src.app import create_app, db


def deploy():
    """Run deployment tasks."""
    app = create_app()
    app.app_context().push()
    db.create_all()

    # migrate database to latest revision
    migrate()
    upgrade()


deploy()
