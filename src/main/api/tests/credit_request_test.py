import pytest


@pytest.mark.api
class TestCreditRequest:
    @pytest.mark.parametrize("amount, term_months", [(5000, 12)])
    def test_credit_request_valid(self, api_manager, created_credit_user_account, amount, term_months):
        user_request, account = created_credit_user_account
        response = api_manager.user_steps.credit_request(user_request, account.id, amount, term_months)

        assert response.amount == amount
        assert response.termMonths == term_months

    @pytest.mark.parametrize("amount, term_months", [(5000, 12)])
    def test_credit_request_user_forbidden(self, api_manager, created_user, created_account, amount, term_months):
        api_manager.user_steps.invalid_credit_request(created_user, created_account.id, amount, term_months)
