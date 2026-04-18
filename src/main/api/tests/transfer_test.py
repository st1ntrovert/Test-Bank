import pytest


@pytest.mark.api
class TestTransfer:
    @pytest.mark.parametrize("transfer_amount", [1000, 3000, 5000])
    def test_transfer(self, api_manager, created_two_accounts_one_with_deposit, transfer_amount):
        first_user, first_account, second_account, deposit_amount = created_two_accounts_one_with_deposit
        response = api_manager.user_steps.transfer_account(first_user, first_account, second_account, transfer_amount)

        assert response.fromAccountId == first_account.id
        assert response.toAccountId == second_account.id
        assert response.fromAccountIdBalance == deposit_amount - transfer_amount

    @pytest.mark.parametrize("transfer_amount", [0, 499, -1])
    def test_transfer_invalid_amount(self, api_manager, created_two_accounts_one_with_deposit, transfer_amount):
        first_user, first_account, second_account, deposit_amount = created_two_accounts_one_with_deposit

        api_manager.user_steps.invalid_transfer_account(first_user, first_account, second_account, transfer_amount)
