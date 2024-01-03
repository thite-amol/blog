"""User model to perform database operations."""

import datetime

import jwt
from flask import current_app as app
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import UserMixin
from marshmallow import Schema, fields, validate

from src.app import db, login_manager


class User(UserMixin, db.Model):
    """User class."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False, unique=True)
    created_on = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False
    )
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    access_token = db.Column(db.String(500), nullable=True, unique=True)

    def __init__(self, **kwargs):
        """The function takes in a dictionary
        of keyword arguments and assigns the values to the class attributes.
        """
        self.username = kwargs.get("username")
        self.email = kwargs.get("email")
        self.password = kwargs.get("password")

    def __repr__(self) -> str:
        """Method to represent user class."""
        return f"<User {self.username}>"

    @staticmethod
    def dump_datetime(value):
        """Deserialize datetime object into string form for JSON processing."""
        if value is None:
            return None
        return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]

    @property
    def serialize(self) -> dict:
        """Return object data in easily serializable format."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "modified_at": self.dump_datetime(self.created_on),
        }

    def hash_password(self) -> None:
        """It takes the password that the user has entered, hashes it, and then stores the hashed password in
        the database.
        """
        self.password = generate_password_hash(self.password).decode("utf8")

    def check_password(self, password: str) -> bool:
        """It takes a plaintext password, hashes it,
         and compares it to the hashed password in the database.

        Args:
            password (str): The password to be checked

        Returns:
            bool: True if hash matched with password
        """
        return check_password_hash(self.password, password)

    def encode_auth_token(self):
        """Generates the Auth Token
        Returns:
            str: Access Token.
        """
        return jwt.encode(
            {
                "id": self.id,
                "email": self.email,
                "username": self.username,
                "exp": datetime.datetime.utcnow()
                + datetime.timedelta(minutes=30),
            },
            app.config.get("SECRET_KEY"),
        )


@login_manager.user_loader
def load_user(userid: int) -> User:
    """Method to load user using id."""
    return User.query.get(userid)


class UserSignupSchema(Schema):
    """Class to validate user input while signup."""

    username = fields.Str(required=True, validate=validate.Length(min=4))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))


class LoginSchema(Schema):
    """Class to validate user input while login."""

    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))


# class ResetPasswordEmailSendSchema(Schema):
#     email = fields.Email(required=True)
#
#
# class ResetPasswordSchema(Schema):
#     password = fields.Str(required=True, validate=validate.Length(min=6))
