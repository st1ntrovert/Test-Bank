import pytest
import requests

from src.main.api.models.requests.login_user_request import LoginUserRequest


@pytest.mark.api
class TestDeposit:
    @pytest.mark.parametrize(
        "username, deposit_amount",
        [
            ("Maxim7", 1000),
            ("Maxim8", 5000),
            ("Maxim9", 9000),
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

        create_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": username,
                "password": "Pas!sw0rd",
                "role": "ROLE_USER"
            },
            headers={
                "accept": "application/json",
                "Content-type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_user_response.status_code == 200
        assert create_user_response.json().get("username") == username
        assert create_user_response.json().get("role") == "ROLE_USER"

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

        create_account_response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_account_response.status_code == 201
        assert create_account_response.json().get("balance") == 0
        created_account_id = create_account_response.json().get("id")

        deposit_response = requests.post(
            url="http://localhost:4111/api/account/deposit",
            json={
                "accountId": created_account_id,
                "amount": deposit_amount
            },
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert deposit_response.status_code == 200
        assert deposit_response.json().get("balance") == deposit_amount

    @pytest.mark.parametrize(
        "username, deposit_amount",
        [
            ("Maximka2222", 999),
            ("Maximka2223", 9001),
            ("Maximka2224", 0),
            ("Maximka2225", ""),
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

        create_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": username,
                "password": "Pas!sw0rd",
                "role": "ROLE_USER"
            },
            headers={
                "accept": "application/json",
                "Content-type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_user_response.status_code == 200
        assert create_user_response.json().get("username") == username
        assert create_user_response.json().get("role") == "ROLE_USER"

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

        create_account_response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_account_response.status_code == 201
        assert create_account_response.json().get("balance") == 0
        created_account_id = create_account_response.json().get("id")

        deposit_response = requests.post(
            url="http://localhost:4111/api/account/deposit",
            json={
                "accountId": created_account_id,
                "amount": deposit_amount
            },
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert deposit_response.status_code == 400
