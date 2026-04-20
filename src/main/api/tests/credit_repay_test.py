from typing import Any

import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit


@pytest.mark.api
class TestCreditRepay:
    @pytest.mark.parametrize("amount", [5000])
    def test_credit_repay_valid(self, api_manager: ApiManager, created_credit: Any, amount: float, db_session: Session):
        user_request, account, credit_data = created_credit
        response = api_manager.user_steps.credit_repay(user_request, credit_data.creditId, account.id, amount)

        assert response.amountDeposited == amount

        credit_from_db = Credit.get_credit_by_account_id(db_session, account.id)
        assert credit_from_db.balance == credit_data.amount - amount, 'Credit balance error'

    @pytest.mark.parametrize("amount", [500])
    def test_credit_repay_invalid(
            self,
            api_manager: ApiManager,
            created_credit: Any,
            amount: float,
            db_session: Session
    ):
        user_request, account, credit_data = created_credit
        api_manager.user_steps.invalid_credit_repay(user_request, credit_data.creditId, account.id, amount)

        credit_from_db = Credit.get_credit_by_account_id(db_session, account.id)
        assert credit_from_db.balance == credit_data.amount, 'Credit change after fail'
