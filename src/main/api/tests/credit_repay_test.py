import pytest


@pytest.mark.api
class TestCreditRepay:
    @pytest.mark.parametrize("amount", [5000])
    def test_credit_repay_valid(self, api_manager, created_credit, amount):
        user_request, account, credit_data = created_credit
        response = api_manager.user_steps.credit_repay(user_request, credit_data.creditId, account.id, amount)

        assert response.amountDeposited == amount

    @pytest.mark.parametrize("amount", [500])
    def test_credit_repay_invalid(self, api_manager, created_credit, amount):
        user_request, account, credit_data = created_credit
        api_manager.user_steps.invalid_credit_repay(user_request, credit_data.creditId, account.id, amount)
