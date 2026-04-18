import pytest


@pytest.mark.api
class TestDeposit:
    @pytest.mark.parametrize("amount", [1000, 5000, 9000])
    def test_deposit_valid(self, api_manager, created_user, created_account, amount):
        response = api_manager.user_steps.deposit_account(created_user, created_account, amount)

        assert response.balance == amount

    @pytest.mark.parametrize("amount", [999, 9001])
    def test_deposit_invalid(self, api_manager, created_user, created_account, amount):
        api_manager.user_steps.invalid_deposit_account(created_user, created_account, amount)
