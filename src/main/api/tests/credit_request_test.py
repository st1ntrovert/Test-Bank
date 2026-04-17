from src.main.api.models.requests.request_credit_request import RequestCreditRequest


class TestCreditRequest:
    def test_credit_request_valid(self, api_manager, create_credit_user_account):
        user_request, account = create_credit_user_account

        request_credit_request = RequestCreditRequest(accountId=account.id, amount=5000, termMonths=12)
        response = api_manager.user_steps.credit_request(user_request, request_credit_request)

        assert request_credit_request.amount == response.amount
        assert request_credit_request.termMonths == response.termMonths

    def test_credit_request_user_forbidden(self, api_manager, create_user_request):
        account = api_manager.user_steps.create_account(create_user_request)
        request_credit_request = RequestCreditRequest(accountId=account.id, amount=5000, termMonths=12)
        api_manager.user_steps.invalid_credit_request(create_user_request, request_credit_request)
