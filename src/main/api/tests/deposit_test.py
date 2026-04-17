import pytest

from src.main.api.models.requests.deposit_request import DepositRequest


@pytest.mark.api
class TestDeposit:
    @pytest.mark.parametrize("amount", [1000, 5000, 9000])
    def test_deposit_valid(self, api_manager, create_user_request, amount):
        account = api_manager.user_steps.create_account(create_user_request)
        deposit_request = DepositRequest(accountId=account.id, amount=amount)
        response = api_manager.user_steps.deposit_account(create_user_request, deposit_request)

        assert response.balance == amount

    @pytest.mark.parametrize("amount", [999, 9001])
    def test_deposit_invalid(self, api_manager, create_user_request, amount):
        account = api_manager.user_steps.create_account(create_user_request)
        deposit_request = DepositRequest(accountId=account.id, amount=amount)
        api_manager.user_steps.invalid_deposit_account(create_user_request, deposit_request)
