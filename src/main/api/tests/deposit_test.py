from typing import Any

import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.requests.create_user_request import CreateUserRequest


@pytest.mark.api
class TestDeposit:
    @pytest.mark.parametrize("amount", [1000, 5000, 9000])
    def test_deposit_valid(
            self,
            api_manager: ApiManager,
            created_user: CreateUserRequest,
            created_account: Any,
            amount: int,
            db_session: Session
    ):
        response = api_manager.user_steps.deposit_account(created_user, created_account, amount)

        assert response.balance == amount

        account_from_db = Account.get_account_by_id(db_session, created_account.id)
        assert account_from_db.balance == amount, 'DB balance still 0'

    @pytest.mark.parametrize("amount", [999, 9001])
    def test_deposit_invalid(
            self,
            api_manager: ApiManager,
            created_user: CreateUserRequest,
            created_account: Any,
            amount: int,
            db_session: Session
    ):
        api_manager.user_steps.invalid_deposit_account(created_user, created_account, amount)

        account_from_db = Account.get_account_by_id(db_session, created_account.id)
        assert account_from_db.balance == 0, 'DB balance increased'
