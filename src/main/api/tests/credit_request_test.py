from typing import Any

import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.models.requests.create_user_request import CreateUserRequest


@pytest.mark.api
class TestCreditRequest:
    @pytest.mark.parametrize("amount, term_months", [(5000, 12)])
    def test_credit_request_valid(
            self,
            api_manager: ApiManager,
            created_credit_user_account: Any,
            amount: float,
            term_months: int,
            db_session: Session
    ):
        user_request, account = created_credit_user_account
        response = api_manager.user_steps.credit_request(user_request, account.id, amount, term_months)

        assert response.amount == amount
        assert response.termMonths == term_months

        credit_from_db = Credit.get_credit_by_account_id(db_session, account.id)
        assert credit_from_db.amount == amount, 'Error with credit request'

    @pytest.mark.parametrize("amount, term_months", [(5000, 12)])
    def test_credit_request_user_forbidden(
            self,
            api_manager: ApiManager,
            created_user: CreateUserRequest,
            created_account: Any,
            amount: float,
            term_months: int,
            db_session: Session
    ):
        api_manager.user_steps.invalid_credit_request(created_user, created_account.id, amount, term_months)

        credit_from_db = Credit.get_credit_by_account_id(db_session, created_account.id)
        assert credit_from_db is None, 'Credit created'
