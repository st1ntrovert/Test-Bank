import pytest


@pytest.mark.api
class TestCreateAccount:
    def test_create_account(self, api_manager, created_user):
        response = api_manager.user_steps.create_account(created_user)

        assert response.balance == 0
