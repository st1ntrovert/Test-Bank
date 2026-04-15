import pytest

from src.main.api.models.requests.create_user_request import CreateUserRequest
from src.main.api.models.requests.deposit_request import DepositRequest
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.deposit_requester import DepositRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestDeposit:
    @pytest.mark.parametrize(
        "username, deposit_amount",
        [
            ("Maxim8", 1000),
            ("Maxim88", 5000),
            ("Maxim888", 9000),
        ])
    def test_deposit_valid(self, username, deposit_amount):
        create_user_request = CreateUserRequest(username=username, password="Pas!sw0rd", role="ROLE_USER")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok(),
        ).post(create_user_request)

        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        deposit_request = DepositRequest(accountId=response.id, amount=deposit_amount)

        response = DepositRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(deposit_request)

        assert response.balance == deposit_amount

    @pytest.mark.parametrize(
        "username, deposit_amount",
        [
            ("Maximka52", 999),
            ("Maximka552", 9001),
            ("Maximka5552", 0),
        ])
    def test_deposit_invalid(self, username, deposit_amount):
        create_user_request = CreateUserRequest(username=username, password="Pas!sw0rd", role="ROLE_USER")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok(),
        ).post(create_user_request)

        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        deposit_request = DepositRequest(accountId=response.id, amount=deposit_amount)

        DepositRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_bad()
        ).post(deposit_request)
