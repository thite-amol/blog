"""Module to test service module."""
import json
from unittest import mock

import pytest

from src.application.user.service import (
    create_user,
    load_user_from_request,
    login_user,
)


def test_create_user_messing_data():
    """Test case to check user creation with missing data."""
    user_data = {"email": "test@test.com", "password": "abcd1234"}
    result = create_user(user_data)

    expected_value = json.loads(
        '{"data": null, "message": [{"error": "username: Missing data for required field."}], "status": false}'
    )
    expected_result = (expected_value, 400)

    assert expected_result == result


class MockQuery:
    """Mock query class to perform query operation."""

    def __init__(self, value):
        """Constructor to set result value."""
        self.result = value

    def first(self):
        """Mock query class first method."""
        return self.result


def test_create_user_email_exist(app):
    """Test case to check user creation with duplicate email."""
    user_data = {
        "username": "testusername",
        "email": "test@test.com",
        "password": "abcd1234",
    }

    def mock_filter_by(*args, **kwargs):
        if kwargs == {"username": "testusername"}:
            return MockQuery(None)
        else:
            return MockQuery(True)

    with app.app_context():
        with mock.patch(
            "flask_sqlalchemy.model._QueryProperty.__get__"
        ) as queryMOCK:  # setup
            queryMOCK.return_value.filter_by.side_effect = mock_filter_by
            result = create_user(user_data)

    expected_result = (
        {
            "data": None,
            "message": [{"error": "Email  already taken"}],
            "status": False,
        },
        400,
    )

    assert expected_result == result


def test_create_user_username_exist(app):
    """Test case to check user creation with duplicate username."""
    user_data = {
        "username": "testusername",
        "email": "test@test.com",
        "password": "abcd1234",
    }

    with app.app_context():
        with mock.patch(
            "flask_sqlalchemy.model._QueryProperty.__get__"
        ) as queryMOCK:  # setup
            queryMOCK.return_value.filter_by.return_value.first.return_value = (
                True
            )
            result = create_user(user_data)

    expected_result = (
        {
            "data": None,
            "message": [{"error": "Username already exist"}],
            "status": False,
        },
        400,
    )

    assert expected_result == result


def test_create_user_valid_data(app):
    """Test case to check user creation with duplicate username."""
    user_data = {
        "username": "testusername",
        "email": "test@test.com",
        "password": "abcd1234",
    }

    with app.app_context():
        with mock.patch(
            "flask_sqlalchemy.model._QueryProperty.__get__"
        ) as queryMOCK:  # setup
            with mock.patch("src.application.user.service.db"):
                queryMOCK.return_value.filter_by.return_value.first.return_value = None
                result = create_user(user_data)

    expected_result = (
        {
            "data": {"email": "test@test.com", "username": "testusername"},
            "message": "User Created",
            "status": True,
        },
        201,
    )

    assert expected_result == result


@pytest.mark.parametrize("user_response", [(True), (None)])
def test_load_user_from_request(app, user_detail, user_response):
    """Test case to check user details wit flask request."""
    mock_request = mock.Mock()
    with app.app_context():
        token = user_detail.encode_auth_token()
        mock_request.headers.get.return_value = "JWT " + token
        with mock.patch(
            "flask_sqlalchemy.model._QueryProperty.__get__"
        ) as queryMOCK:  # setup
            if user_response:
                queryMOCK.return_value.filter_by.return_value.first.return_value = user_detail
                result = load_user_from_request(mock_request)

                assert result == user_detail
            else:
                queryMOCK.return_value.filter_by.return_value.first.return_value = None
                result = load_user_from_request(mock_request)

                assert result is None


@pytest.mark.parametrize(
    "token",
    [
        (
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6bnVsbCwiZW1haWwiOiJ0ZXN0QHRlc3QuY29tIiwidXNlcm5hbWUiOiJ0ZXN0X3VzZXJuYW1lIiwiZXhwIjoxNjcyNzI5NjA3fQ.MgGkY0DBxXPXcrrpMVH5w0PbEt3spxdB7EPN2tb1gYE"
        ),
        ("invalid-token"),
    ],
)
def test_load_user_from_request_exception(app, user_detail, token):
    """Test case to check user details wit flask request Exception."""
    mock_request = mock.Mock()
    with app.app_context():
        mock_request.headers.get.return_value = "JWT " + token
        with mock.patch(
            "flask_sqlalchemy.model._QueryProperty.__get__"
        ) as queryMOCK:  # setup
            queryMOCK.return_value.filter_by.return_value.first.return_value = (
                user_detail
            )
            result = load_user_from_request(mock_request)

        assert result is None


@pytest.mark.parametrize(
    ("user_input", "expected_status", "expected_data"),
    [
        (
            {"email": "test@test.com"},
            400,
            {
                "data": None,
                "message": [
                    {"error": "password: Missing data for required field."}
                ],
                "status": False,
            },
        ),
        (
            {"email": "test@test.com", "password": "abcd56"},
            400,
            {
                "data": None,
                "message": [{"error": "Invalid username or password"}],
                "status": False,
            },
        ),
    ],
)
def test_user_login(
    app, user_detail, user_input, expected_status, expected_data
):
    """Test case to validate user details."""
    with app.app_context():
        with mock.patch(
            "flask_sqlalchemy.model._QueryProperty.__get__"
        ) as queryMOCK:  # setup
            queryMOCK.return_value.filter_by.return_value.first.return_value = (
                user_detail
            )
            response = login_user(user_input)

    assert response[0] == expected_data
    assert response[1] == expected_status
