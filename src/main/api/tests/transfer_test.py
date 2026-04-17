from src.main.api.models.requests.transfer_request import TransferRequest


class TestTransfer:
    def test_transfer(self, api_manager, create_two_accounts_with_deposit):
        first_user_request, first_account, second_account = create_two_accounts_with_deposit
        transfer_request = TransferRequest(fromAccountId=first_account.id, toAccountId=second_account.id, amount=3000)
        response = api_manager.user_steps.transfer_account(first_user_request, transfer_request)

        assert response.fromAccountId == first_account.id
        assert response.toAccountId == second_account.id
        assert response.fromAccountIdBalance == 2000

    def test_transfer_invalid_amount(self, api_manager, create_two_accounts_with_deposit):
        first_user_request, first_account, second_account = create_two_accounts_with_deposit
        transfer_request = TransferRequest(fromAccountId=first_account.id, toAccountId=second_account.id, amount=499)
        api_manager.user_steps.invalid_transfer_account(first_user_request, transfer_request)
