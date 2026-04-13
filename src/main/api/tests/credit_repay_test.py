import requests

from src.main.api.models.requests.create_user_request import CreateUserRequest
from src.main.api.models.requests.login_user_request import LoginUserRequest
from src.main.api.models.requests.repay_credit_request import RepayCreditRequest
from src.main.api.models.requests.request_credit_request import RequestCreditRequest
from src.main.api.models.responses.create_account_response import CreateAccountResponse
from src.main.api.models.responses.create_user_response import CreateUserResponse
from src.main.api.models.responses.repay_credit_response import RepayCreditResponse
from src.main.api.models.responses.request_credit_response import RequestCreditResponse


class TestCreditRepay:
    def test_credit_repay_valid(self):
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

        create_user_request = CreateUserRequest(username="MaxRepay", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")

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

        login_user_request = LoginUserRequest(username="MaxRepay", password="Pas!sw0rd")

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
        account_id = create_account_response.id

        request_credit_request = RequestCreditRequest(accountId=account_id,amount=5000, termMonths=12)

        response = requests.post(
            url="http://localhost:4111/api/credit/request",
            json=request_credit_request.model_dump(),
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert response.status_code == 201
        request_credit_response = RequestCreditResponse(**response.json())
        assert request_credit_request.amount == request_credit_response.amount
        assert request_credit_request.termMonths == request_credit_response.termMonths
        credit_id = request_credit_response.creditId

        repay_credit_request = RepayCreditRequest(creditId=credit_id, accountId=account_id, amount=5000)

        response = requests.post(
            url="http://localhost:4111/api/credit/repay",
            json=repay_credit_request.model_dump(),
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert response.status_code == 200
        repay_credit_response = RepayCreditResponse(**response.json())
        assert repay_credit_request.amount == repay_credit_response.amountDeposited

    def test_credit_repay_invalid(self):
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

        create_user_request = CreateUserRequest(username="MaxNoRepay3", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")

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

        login_user_request = LoginUserRequest(username="MaxNoRepay3", password="Pas!sw0rd")

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
        account_id = create_account_response.id

        request_credit_request = RequestCreditRequest(accountId=account_id, amount=5000, termMonths=12)

        response = requests.post(
            url="http://localhost:4111/api/credit/request",
            json=request_credit_request.model_dump(),
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert response.status_code == 201
        request_credit_response = RequestCreditResponse(**response.json())
        assert request_credit_request.amount == request_credit_response.amount
        assert request_credit_request.termMonths == request_credit_response.termMonths
        credit_id = request_credit_response.creditId

        repay_credit_request = RepayCreditRequest(creditId=credit_id, accountId=account_id, amount=500)

        response = requests.post(
            url="http://localhost:4111/api/credit/repay",
            json=repay_credit_request.model_dump(),
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert response.status_code == 422