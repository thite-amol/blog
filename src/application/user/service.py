"""Perform all user related operations."""

from typing import Union

import jwt
from flask import current_app as app
from flask_login import current_user

from src.app import db, login_manager
from src.application.user.model import (
    LoginSchema,
    User,
    UserSignupSchema,
)
from src.util import generate_response


def create_user(input_data: dict) -> tuple:
    """Method to create user with given data.

    Args:
        input_data (dict): Required user data to create user object.

    Returns:
        tuple: A response object
    """
    create_validation_schema = UserSignupSchema()
    errors = create_validation_schema.validate(input_data)

    if errors:
        return generate_response(message=errors)

    check_username_exist = User.query.filter_by(
        username=input_data.get("username")
    ).first()

    if check_username_exist:
        return generate_response(message="Username already exist", status=400)

    check_email_exist = User.query.filter_by(
        email=input_data.get("email")
    ).first()
    if check_email_exist:
        return generate_response(message="Email  already taken", status=400)

    new_user = User(**input_data)
    new_user.hash_password()
    db.session.add(new_user)
    db.session.commit()
    del input_data["password"]

    return generate_response(
        data=input_data, message="User Created", status=201
    )


def login_user(input_data: dict) -> tuple:
    """Method to login user with given data.

    Args:
        input_data (dict): Required user data to create user object.

    Returns:
        tuple: A response object
    """
    create_validation_schema = LoginSchema()
    errors = create_validation_schema.validate(input_data)
    if errors:
        return generate_response(message=errors)

    user_details = User.query.filter_by(email=input_data.get("email")).first()

    if (user_details is None) or not user_details.check_password(
        input_data.get("password")
    ):
        return generate_response(
            message="Invalid username or password", status=400
        )

    token = user_details.encode_auth_token()

    return generate_response(
        data={"access_token": token},
        message="User login successfully",
        status=201,
    )


@login_manager.request_loader
def load_user_from_request(request) -> Union[None, User]:
    """Method take JWT user token from header and try to authenticate user based on given details.

    Args:
        request : Flask request object.

    Returns:
        Union[None, User]: User details if user provides valid token otherwise None
    """
    auth_headers = request.headers.get("Authorization", "").split()
    if len(auth_headers) != 2:
        return None
    try:
        token = auth_headers[1]
        data = jwt.decode(
            token, app.config.get("SECRET_KEY"), algorithms=["HS256"]
        )
        user = User.query.filter_by(email=data["email"]).first()
        if user:
            return user
    except jwt.ExpiredSignatureError:
        return None
    except (jwt.InvalidTokenError, Exception):  # pylint: disable=broad-except
        return None

    return None


def get_current_user() -> tuple:
    """Method to load current user.

    Returns:
        tuple: A response object
    """
    if current_user.is_authenticated:
        return generate_response(
            data=current_user.serialize,
            status=200,
        )

    return generate_response(data=User().serialize, status=200)
