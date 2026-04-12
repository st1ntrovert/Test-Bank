import pytest
import requests

from src.main.api.models.responses.create_account_response import CreateAccountResponse
from src.main.api.models.requests.create_user_request import CreateUserRequest
from src.main.api.models.requests.login_user_request import LoginUserRequest


@pytest.mark.api
class TestCreateAccount:
    def test_create_account(self):
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

        create_user_request = CreateUserRequest(username="Max11x", password="Pas!sw0rd", role="ROLE_USER")

        create_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json=create_user_request.model_dump(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_user_response.status_code == 200

        login_user_request = LoginUserRequest(username="Max11x", password="Pas!sw0rd")

        login_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=login_user_request.model_dump(),
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
        )

        assert login_user_response.status_code == 200
        token = login_user_response.json().get("token")

        response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert response.status_code == 201
        create_account_response = CreateAccountResponse(**response.json())
        assert create_account_response.balance == 0
