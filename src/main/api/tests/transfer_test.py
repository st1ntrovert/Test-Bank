import requests

from src.main.api.models.requests.create_user_request import CreateUserRequest
from src.main.api.models.requests.deposit_request import DepositRequest
from src.main.api.models.requests.login_user_request import LoginUserRequest
from src.main.api.models.requests.transfer_request import TransferRequest
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.deposit_requester import DepositRequester
from src.main.api.requests.transfer_requester import TransferRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


class TestTransfer:
    def test_transfer(self):
        create_first_user_request = CreateUserRequest(username="MaximFirst4", password="Pas!sw0rd", role="ROLE_USER")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_first_user_request)

        first_user_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="MaximFirst4", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        deposit_request = DepositRequest(accountId= first_user_response.id, amount=5000)

        DepositRequester(
            request_spec=RequestSpecs.auth_headers(username="MaximFirst4", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(deposit_request)

        create_second_user_request = CreateUserRequest(username="MaximSecond4", password="Pas!sw0rd", role="ROLE_USER")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_second_user_request)

        second_user_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="MaximSecond4", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        transfer_request = TransferRequest(
            fromAccountId=first_user_response.id,
            toAccountId=second_user_response.id,
            amount=3000,
        )

        response = TransferRequester(
            request_spec=RequestSpecs.auth_headers(username="MaximFirst4", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(transfer_request)

        assert response.fromAccountId == first_user_response.id
        assert response.toAccountId == second_user_response.id
        assert response.fromAccountIdBalance == 5000 - 3000

    def test_transfer_invalid_amount(self):
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
        admin_token = login_admin_response.json().get("token")

        create_user_request = CreateUserRequest(username="MaxInvalid3", password="Pas!sw0rd", role="ROLE_USER" )

        response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json=create_user_request.model_dump(),
            headers={
                "accept": "application/json",
                "Content-type": "application/json",
                "Authorization": f"Bearer {admin_token}"
            }
        )
        assert response.status_code == 200

        login_user_request = LoginUserRequest(username="MaxInvalid3", password="Pas!sw0rd")

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

        account1 = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        assert account1.status_code == 201
        account1_id = account1.json().get("id")

        account2 = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        assert account2.status_code == 201
        account2_id = account2.json().get("id")

        deposit_request = DepositRequest(accountId=account1_id, amount=5000)

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

        transfer_request = TransferRequest(fromAccountId=account1_id, toAccountId=account2_id, amount=499)

        response = requests.post(
            url="http://localhost:4111/api/account/transfer",
            json=transfer_request.model_dump(),
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert response.status_code == 400
