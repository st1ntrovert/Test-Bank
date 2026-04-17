import pytest

from src.main.api.models.requests.create_user_request import CreateUserRequest
from src.main.api.models.requests.deposit_request import DepositRequest


@pytest.fixture
def create_user_request(api_manager):
    user_request = CreateUserRequest(username="MaxTheTester", password="Pas!sw0rd", role="ROLE_USER")
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def create_two_users_request(api_manager):
    first_user_request = CreateUserRequest(username="MaxTheFirst", password="Pas!sw0rd", role="ROLE_USER")
    second_user_request = CreateUserRequest(username="MaxTheSecond", password="Pas!sw0rd", role="ROLE_USER")
    api_manager.admin_steps.create_user(first_user_request)
    api_manager.admin_steps.create_user(second_user_request)
    return first_user_request, second_user_request

@pytest.fixture
def create_two_accounts_with_deposit(api_manager, create_two_users_request):
    first_user_request, second_user_request = create_two_users_request
    first_account = api_manager.user_steps.create_account(first_user_request)
    second_account = api_manager.user_steps.create_account(second_user_request)
    api_manager.user_steps.deposit_account(
        first_user_request,
        DepositRequest(accountId=first_account.id, amount=5000)
    )
    return first_user_request, first_account, second_account

@pytest.fixture
def create_credit_user_account(api_manager):
    user_request = CreateUserRequest(username="MaxTheCredit", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")
    api_manager.admin_steps.create_user(user_request)
    account = api_manager.user_steps.create_account(user_request)
    return user_request, account