import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account


@pytest.mark.api
class TestCreateAccount:
    def test_create_account(self, api_manager: ApiManager, created_user, db_session):
        response = api_manager.user_steps.create_account(created_user)

        assert response.balance == 0

        account_from_db = Account.get_account_by_id(db_session, response.id)
        assert account_from_db.id == response.id, 'Account id not in DB'
        assert account_from_db.balance is not None, 'No balance in DB'