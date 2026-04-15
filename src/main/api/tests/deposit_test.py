import pytest
import requests

from src.main.api.models.requests.create_user_request import CreateUserRequest
from src.main.api.models.requests.deposit_request import DepositRequest
from src.main.api.models.requests.login_user_request import LoginUserRequest
from src.main.api.models.responses.create_account_response import CreateAccountResponse
from src.main.api.models.responses.create_user_response import CreateUserResponse
from src.main.api.models.responses.deposit_response import DepositResponse


@pytest.mark.api
class TestDeposit:
    @pytest.mark.parametrize(
        "username, deposit_amount",
        [
            ("Maxim5", 1000),
            ("Maxim55", 5000),
            ("Maxim555", 9000),
        ])
    def test_deposit_valid(self, username, deposit_amount):
        login_admin_request = LoginUserRequest(username="admin", password="123456")

        login_admin_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=login_admin_request.model_dump(),
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            }
        )

        assert login_admin_response.status_code == 200
        token = login_admin_response.json().get("token")

        create_user_request = CreateUserRequest(username=username, password="Pas!sw0rd", role="ROLE_USER")

        response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json=create_user_request.model_dump(),
            headers={
                "accept": "application/json",
                "Content-type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert response.status_code == 200
        create_user_response = CreateUserResponse(**response.json())
        assert create_user_request.username == create_user_response.username
        assert create_user_request.role == create_user_response.role

        login_user_request = LoginUserRequest(username=username, password="Pas!sw0rd")

        login_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=login_user_request.model_dump(),
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            }
        )

        assert login_user_response.status_code == 200
        token = login_user_response.json().get("token")

        response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert response.status_code == 201
        create_account_response = CreateAccountResponse(**response.json())
        assert create_account_response.balance == 0
        created_account_id = create_account_response.id

        deposit_request = DepositRequest(accountId=created_account_id, amount=deposit_amount)

        response = requests.post(
            url="http://localhost:4111/api/account/deposit",
            json=deposit_request.model_dump(),
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert response.status_code == 200
        deposit_response = DepositResponse(**response.json())
        assert deposit_response.balance == deposit_request.amount

    @pytest.mark.parametrize(
        "username, deposit_amount",
        [
            ("Maximka5", 999),
            ("Maximka55", 9001),
            ("Maximka555", 0),
        ])
    def test_deposit_invalid(self, username, deposit_amount):
        login_admin_request = LoginUserRequest(username="admin", password="123456")

        login_admin_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=login_admin_request.model_dump(),
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            }
        )

        assert login_admin_response.status_code == 200
        token = login_admin_response.json().get("token")

        create_user_request = CreateUserRequest(username=username, password="Pas!sw0rd", role="ROLE_USER")

        response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json=create_user_request.model_dump(),
            headers={
                "accept": "application/json",
                "Content-type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert response.status_code == 200
        create_user_response = CreateUserResponse(**response.json())
        assert create_user_response.username == create_user_request.username
        assert create_user_response.role == create_user_request.role

        login_user_request = LoginUserRequest(username=username, password="Pas!sw0rd")

        login_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=login_user_request.model_dump(),
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            }
        )

        assert login_user_response.status_code == 200
        token = login_user_response.json().get("token")

        response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert response.status_code == 201
        create_account_response = CreateAccountResponse(**response.json())
        assert create_account_response.balance == 0
        created_account_id = create_account_response.id

        deposit_request = DepositRequest(accountId=created_account_id, amount=deposit_amount)

        deposit_response = requests.post(
            url="http://localhost:4111/api/account/deposit",
            json=deposit_request.model_dump(),
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert deposit_response.status_code == 400
