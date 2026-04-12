import requests
import pytest

from src.main.api.models.requests.create_user_request import CreateUserRequest
from src.main.api.models.requests.login_user_request import LoginUserRequest
from src.main.api.models.responses.login_user_response import LoginUserResponse
from src.main.api.requests.login_user_requester import LoginUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestUserLogin:
    def test_login_admin(self):
        login_user_request = LoginUserRequest(username="admin", password="123456")

        response = LoginUserRequester(
            request_spec=RequestSpecs.unauthorized_headers(),
            response_spec=ResponseSpecs.request_ok(),
        ).post(login_user_request)

        assert login_user_request.username == response.user.username
        assert response.user.role == "ROLE_ADMIN"

    def test_login_user(self):
        login_user_request = LoginUserRequest(username="admin", password="123456")

        login_admin_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=login_user_request.model_dump(),
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )

        assert login_admin_response.status_code == 200
        token = login_admin_response.json().get("token")

        create_user_request = CreateUserRequest(username="Max1x", password="Pas!sw0rd", role="ROLE_USER")

        create_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json=create_user_request.model_dump(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_user_response.status_code == 200

        login_user_request = LoginUserRequest(username="Max1x", password="Pas!sw0rd")

        response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=login_user_request.model_dump(),
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
        )

        assert response.status_code == 200
        login_user_response = LoginUserResponse(**response.json())

        assert login_user_request.username == login_user_response.user.username
        assert login_user_response.user.role == "ROLE_USER"
