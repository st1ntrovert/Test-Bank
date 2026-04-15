import requests

from src.main.api.models.requests.create_user_request import CreateUserRequest
from src.main.api.models.requests.deposit_request import DepositRequest
from src.main.api.models.requests.login_user_request import LoginUserRequest
from src.main.api.models.requests.transfer_request import TransferRequest
from src.main.api.models.responses.create_account_response import CreateAccountResponse
from src.main.api.models.responses.create_user_response import CreateUserResponse
from src.main.api.models.responses.deposit_response import DepositResponse
from src.main.api.models.responses.transfer_response import TransferResponse


class TestTransfer:
    def test_transfer(self):
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

        create_first_user_request = CreateUserRequest(username="MaximFirst3", password="Pas!sw0rd", role="ROLE_USER")

        response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json=create_first_user_request.model_dump(),
            headers={
                "accept": "application/json",
                "Content-type": "application/json",
                "Authorization": f"Bearer {admin_token}"
            }
        )

        assert response.status_code == 200
        create_first_user_response = CreateUserResponse(**response.json())
        assert create_first_user_response.username == create_first_user_request.username
        assert create_first_user_response.role == create_first_user_request.role

        create_second_user_request = CreateUserRequest(username="MaximSecond3", password="Pas!sw0rd", role="ROLE_USER")

        response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json=create_second_user_request.model_dump(),
            headers={
                "accept": "application/json",
                "Content-type": "application/json",
                "Authorization": f"Bearer {admin_token}"
            }
        )

        assert response.status_code == 200
        create_second_user_response = CreateUserResponse(**response.json())
        assert create_second_user_response.username == create_second_user_request.username
        assert create_second_user_response.role == create_second_user_request.role

        login_user_request = LoginUserRequest(username="MaximSecond3", password="Pas!sw0rd")

        login_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=login_user_request.model_dump(),
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            }
        )

        assert login_user_response.status_code == 200
        second_user_token = login_user_response.json().get("token")

        response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {second_user_token}"
            }
        )

        assert response.status_code == 201
        create_account_response = CreateAccountResponse(**response.json())
        assert create_account_response.balance == 0
        second_account_id = create_account_response.id

        login_user_request = LoginUserRequest(username="MaximFirst3", password="Pas!sw0rd")

        login_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=login_user_request.model_dump(),
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            }
        )

        assert login_user_response.status_code == 200
        first_user_token = login_user_response.json().get("token")

        response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {first_user_token}"
            }
        )

        assert response.status_code == 201
        create_account_response = CreateAccountResponse(**response.json())
        assert create_account_response.balance == 0
        first_account_id = create_account_response.id

        deposit_request = DepositRequest(accountId= first_account_id, amount=5000)

        response = requests.post(
            url="http://localhost:4111/api/account/deposit",
            json=deposit_request.model_dump(),
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {first_user_token}"
            }
        )

        assert response.status_code == 200
        deposit_response = DepositResponse(**response.json())
        assert deposit_response.balance == deposit_request.amount

        transfer_request = TransferRequest(fromAccountId=first_account_id, toAccountId=second_account_id, amount=3000)

        response = requests.post(
            url="http://localhost:4111/api/account/transfer",
            json=transfer_request.model_dump(),
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {first_user_token}",
                "Content-Type": "application/json"
            }
        )

        assert response.status_code == 200
        transfer_response = TransferResponse(**response.json())
        assert transfer_response.fromAccountIdBalance == deposit_response.balance - transfer_request.amount

        transactions_response = requests.get(
            url=f"http://localhost:4111/api/account/transactions/{second_account_id}",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {second_user_token}"
            }
        )

        assert transactions_response.status_code == 200
        transactions = transactions_response.json().get("transactions")
        assert any(t.get("type") == "transfer_in" and t.get("amount") == 3000 for t in transactions)
        assert transactions_response.json().get("balance") == 3000

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
