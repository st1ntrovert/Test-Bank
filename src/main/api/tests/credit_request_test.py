from src.main.api.models.requests.create_user_request import CreateUserRequest
from src.main.api.models.requests.request_credit_request import RequestCreditRequest
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.credit_requester import CreditRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


class TestCreditRequest:
    def test_credit_request_valid(self):
        create_user_request = CreateUserRequest(username="Max56", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok(),
        ).post(create_user_request)

        account_data = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max56", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        request_credit_request = RequestCreditRequest(accountId=account_data.id, amount=5000, termMonths=12)

        response = CreditRequester(
            request_spec=RequestSpecs.auth_headers(username="Max56", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post(request_credit_request)

        assert request_credit_request.amount == response.amount
        assert request_credit_request.termMonths == response.termMonths

    def test_credit_request_user_forbidden(self):
        create_user_request = CreateUserRequest(username="MaxNotCredit2", password="Pas!sw0rd", role="ROLE_USER")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok(),
        ).post(create_user_request)

        account_data = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="MaxNotCredit2", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        request_credit_request = RequestCreditRequest(accountId=account_data.id, amount=5000, termMonths=12)

        CreditRequester(
            request_spec=RequestSpecs.auth_headers(username="MaxNotCredit2", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_forbidden()
        ).post(request_credit_request)
