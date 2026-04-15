from src.main.api.models.requests.create_user_request import CreateUserRequest
from src.main.api.models.requests.repay_credit_request import RepayCreditRequest
from src.main.api.models.requests.request_credit_request import RequestCreditRequest
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.credit_repay_requester import CreditRepayRequester
from src.main.api.requests.credit_requester import CreditRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


class TestCreditRepay:
    def test_credit_repay_valid(self):
        create_user_request = CreateUserRequest(username="MaxRepay2", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok(),
        ).post(create_user_request)

        account_data = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="MaxRepay2", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        request_credit_request = RequestCreditRequest(accountId=account_data.id, amount=5000, termMonths=12)

        credit_data = CreditRequester(
            request_spec=RequestSpecs.auth_headers(username="MaxRepay2", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post(request_credit_request)

        repay_credit_request = RepayCreditRequest(creditId=credit_data.creditId, accountId=credit_data.id, amount=5000)

        response = CreditRepayRequester(
            request_spec=RequestSpecs.auth_headers(username="MaxRepay2", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(repay_credit_request)

        assert repay_credit_request.amount == response.amountDeposited

    def test_credit_repay_invalid(self):
        create_user_request = CreateUserRequest(username="MaxNoRepay5", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok(),
        ).post(create_user_request)

        account_data = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="MaxNoRepay5", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        request_credit_request = RequestCreditRequest(accountId=account_data.id, amount=5000, termMonths=12)

        credit_data = CreditRequester(
            request_spec=RequestSpecs.auth_headers(username="MaxNoRepay5", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post(request_credit_request)

        repay_credit_request = RepayCreditRequest(creditId=credit_data.creditId, accountId=credit_data.id, amount=500)

        CreditRepayRequester(
            request_spec=RequestSpecs.auth_headers(username="MaxNoRepay5", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_unprocessable()
        ).post(repay_credit_request)
