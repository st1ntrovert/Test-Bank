import pytest


@pytest.mark.api
class TestUserLogin:
    def test_login_admin(self, api_manager, login_admin_data):
        response = api_manager.admin_steps.login_user(login_admin_data)

        assert login_admin_data.username == response.user.username
        assert response.user.role == "ROLE_ADMIN"

    def test_login_user(self, api_manager, created_user):
        response = api_manager.admin_steps.login_user(created_user)

        assert created_user.username == response.user.username
        assert response.user.role == "ROLE_USER"
