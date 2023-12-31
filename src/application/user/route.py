"""Defines all the user routes."""

from flask import Blueprint, make_response, request

from src.application.user.service import (
    create_user,
    get_current_user,
    login_user,
)

user = Blueprint(
    "user",
    __name__,
    static_folder="static",
    template_folder="templates",
    url_prefix="/user",
)


@user.get("/")
def index():
    """Method to get the user details
    Returns:
        User details.
    """
    response, status = get_current_user()
    return make_response(response, status)


@user.post("/")
def store_user():
    """Post method to create user in system
    Returns:
        json.
    """
    input_data = request.get_json()
    response, status = create_user(input_data)
    return make_response(response, status)


@user.post("/login")
def user_auth():
    """Post method to get user access token
    Returns:
        json.
    """
    input_data = request.get_json()
    response, status = login_user(input_data)
    return make_response(response, status)
