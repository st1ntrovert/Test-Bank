import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account


@pytest.mark.api
class TestTransfer:
    @pytest.mark.parametrize("transfer_amount", [1000, 3000, 5000])
    def test_transfer(
            self,
            api_manager: ApiManager,
            created_two_accounts_one_with_deposit: tuple,
            transfer_amount: float,
            db_session: Session
    ):
        first_user, first_account, second_account, deposit_amount = created_two_accounts_one_with_deposit
        response = api_manager.user_steps.transfer_account(first_user, first_account, second_account, transfer_amount)

        assert response.fromAccountId == first_account.id
        assert response.toAccountId == second_account.id
        assert response.fromAccountIdBalance == deposit_amount - transfer_amount

        first_account_from_db = Account.get_account_by_id(db_session, first_account.id)
        second_account_from_db = Account.get_account_by_id(db_session, second_account.id)
        assert first_account_from_db.balance == deposit_amount - transfer_amount, 'Sender balance the same'
        assert second_account_from_db.balance == transfer_amount, 'Receiver balance the same'

    @pytest.mark.parametrize("transfer_amount", [0, 499, -1])
    def test_transfer_invalid_amount(
            self,
            api_manager: ApiManager,
            created_two_accounts_one_with_deposit: tuple,
            transfer_amount: float,
            db_session: Session
    ):
        first_user, first_account, second_account, deposit_amount = created_two_accounts_one_with_deposit

        api_manager.user_steps.invalid_transfer_account(first_user, first_account, second_account, transfer_amount)

        first_account_from_db = Account.get_account_by_id(db_session, first_account.id)
        second_account_from_db = Account.get_account_by_id(db_session, second_account.id)
        assert first_account_from_db.balance == deposit_amount, 'Sender balance decreased'
        assert second_account_from_db.balance == 0, 'Receiver balance increased'
