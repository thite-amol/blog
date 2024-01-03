"""route testing module."""
import json
from unittest import mock

from src.util import generate_response


@mock.patch("flask_login.utils._get_user")
def test_user_details(current_user, client, user_detail):
    """Test logged in user details."""
    current_user.return_value = user_detail
    response = client.get("/user/")
    expected_value = json.loads(
        '{"data": {"email": "test@test.com","id": null,"modified_at": null,"username": "test_username"},"message": [],"status": true}'
    )
    actual_dict = json.loads(response.data)

    assert response.status_code == 200

    assert expected_value == actual_dict


def test_user_details_guest(client):
    """Test guest user details."""
    response = client.get("/user/")

    expected_value = json.loads(
        '{"data": {"email": null,"id": null,"modified_at": null,"username": null},"message": [],"status": true}'
    )
    actual_dict = json.loads(response.data)

    assert response.status_code == 200

    assert expected_value == actual_dict


def test_user_auth(app, client, user_detail):
    """Test user Login."""
    with app.app_context():
        with mock.patch(
            "flask_sqlalchemy.model._QueryProperty.__get__"
        ) as queryMOCK:  # setup
            queryMOCK.return_value.filter_by.return_value.first.return_value = (
                user_detail
            )

            response = client.post(
                "/user/login",
                data=json.dumps(
                    {"email": "test@test.com", "password": "abcd1234"}
                ),
                content_type="application/json",
            )

    assert str(user_detail) == "<User test_username>"
    assert response.status_code == 201


def test_user_register_route(app, client, user_detail):
    """Test user registration."""
    with mock.patch("src.application.user.route.create_user") as mocked_create:
        mocked_create.return_value = generate_response(
            data=None, message="User Created", status=201
        )
        response = client.post(
            "/user/",
            data=json.dumps({"email": "test@test.com", "password": "abcd1234"}),
            content_type="application/json",
        )

    assert response.status_code == 201
