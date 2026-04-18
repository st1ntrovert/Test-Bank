import pytest

from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.requests.create_credit_user_request import CreateCreditUserRequest
from src.main.api.models.requests.create_user_request import CreateUserRequest
from src.main.api.models.requests.login_user_request import LoginUserRequest


@pytest.fixture
def created_user(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request


@pytest.fixture
def created_account(api_manager, created_user):
    account = api_manager.user_steps.create_account(created_user)
    return account


@pytest.fixture
def login_admin_data(api_manager):
    response = LoginUserRequest(username="admin", password="123456")
    return response


@pytest.fixture
def created_two_users(api_manager, created_user):
    second_user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(second_user_request)
    return created_user, second_user_request


@pytest.fixture
def created_two_accounts_one_with_deposit(api_manager, created_two_users):
    first_user, second_user = created_two_users

    deposit_amount = 5000

    first_account = api_manager.user_steps.create_account(first_user)
    second_account = api_manager.user_steps.create_account(second_user)

    api_manager.user_steps.deposit_account(first_user, first_account, deposit_amount)

    return first_user, first_account, second_account, deposit_amount


@pytest.fixture
def created_credit_user(api_manager):
    user_request = RandomModelGenerator.generate(CreateCreditUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def created_credit_user_account(api_manager, created_credit_user):
    account = api_manager.user_steps.create_account(created_credit_user)
    return created_credit_user, account


@pytest.fixture
def created_credit(api_manager, created_credit_user_account):
    user_request, account = created_credit_user_account
    credit = api_manager.user_steps.credit_request(user_request, account.id, 5000, 12)
    return user_request, account, credit