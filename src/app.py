"""This module is used to bootstrap flask application."""

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import (
    LoginManager,
)
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

login_manager = LoginManager()
# login_manager.session_protection = "strong"
# login_manager.login_message_category = "info"

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
marshmallow = Marshmallow()


def create_app() -> Flask:
    """Create a flask application object with dependencies.

    Returns:
        Flask app object
    """
    flask_app = Flask(__name__)

    flask_app.config.from_object("src.config.Config")
    login_manager.init_app(flask_app)
    db.init_app(flask_app)
    migrate.init_app(flask_app, db)
    bcrypt.init_app(flask_app)
    marshmallow.init_app(flask_app)
    from src.application.user.route import user  # pylint: disable=C

    flask_app.register_blueprint(user)

    return flask_app


app = create_app()


@app.route("/")
def health() -> dict:
    """Method to check current application health.

    Returns:
        dictionary
    """
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="127.0.0.1")
