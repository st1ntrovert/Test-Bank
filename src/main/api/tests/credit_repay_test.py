from src.main.api.models.requests.repay_credit_request import RepayCreditRequest
from src.main.api.models.requests.request_credit_request import RequestCreditRequest


class TestCreditRepay:
    def test_credit_repay_valid(self, api_manager, create_credit_user_account):
        user_request, account = create_credit_user_account

        credit_data = api_manager.user_steps.credit_request(
            user_request,
            RequestCreditRequest(accountId=account.id, amount=5000, termMonths=12)
        )

        repay_request = RepayCreditRequest(creditId=credit_data.creditId, accountId=account.id, amount=5000)
        response = api_manager.user_steps.credit_repay(user_request, repay_request)

        assert repay_request.amount == response.amountDeposited

    def test_credit_repay_invalid(self, api_manager, create_credit_user_account):
        user_request, account = create_credit_user_account

        credit_data = api_manager.user_steps.credit_request(
            user_request,
            RequestCreditRequest(accountId=account.id, amount=5000, termMonths=12)
        )

        repay_request = RepayCreditRequest(creditId=credit_data.creditId, accountId=account.id, amount=500)
        api_manager.user_steps.invalid_credit_repay(user_request, repay_request)
