from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validated_crud_requester import ValidatedCrudRequester
from src.main.api.models.requests.create_user_request import CreateUserRequest
from src.main.api.models.requests.deposit_request import DepositRequest
from src.main.api.models.requests.repay_credit_request import RepayCreditRequest
from src.main.api.models.requests.request_credit_request import RequestCreditRequest
from src.main.api.models.requests.transfer_request import TransferRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        response = ValidatedCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.ACCOUNT_CREATE,
            ResponseSpecs.request_created()
        ).post()
        return response

    def deposit_account(self, create_user_request: CreateUserRequest, account, amount):
        deposit_request = DepositRequest(accountId=account.id, amount=amount)
        response = ValidatedCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.ACCOUNT_DEPOSIT,
            ResponseSpecs.request_ok()
        ).post(deposit_request)
        return response

    def invalid_deposit_account(self, create_user_request: CreateUserRequest, account, amount):
        deposit_request = DepositRequest(accountId=account.id, amount=amount)
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.ACCOUNT_DEPOSIT,
            ResponseSpecs.request_bad()
        ).post(deposit_request)
        return response

    def transfer_account(self, create_user_request: CreateUserRequest, from_account, to_account, amount: float):
        transfer_request = TransferRequest(fromAccountId=from_account.id, toAccountId=to_account.id, amount=amount)
        response = ValidatedCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.ACCOUNT_TRANSFER,
            ResponseSpecs.request_ok()
        ).post(transfer_request)
        return response

    def invalid_transfer_account(self, create_user_request: CreateUserRequest, from_account, to_account, amount):
        transfer_request = TransferRequest(fromAccountId=from_account.id, toAccountId=to_account.id, amount=amount)
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.ACCOUNT_TRANSFER,
            ResponseSpecs.request_bad()
        ).post(transfer_request)
        return response

    def credit_request(self, create_user_request: CreateUserRequest, account_id, amount, term_months):
        credit_request = RequestCreditRequest(accountId=account_id, amount=amount, termMonths=term_months)
        response = ValidatedCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.REQUEST_CREDIT,
            ResponseSpecs.request_created()
        ).post(credit_request)
        return response

    def invalid_credit_request(self, create_user_request: CreateUserRequest, account_id, amount, term_months):
        credit_request = RequestCreditRequest(accountId=account_id, amount=amount, termMonths=term_months)
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.REQUEST_CREDIT,
            ResponseSpecs.request_forbidden()
        ).post(credit_request)
        return response

    def credit_repay(self, create_user_request: CreateUserRequest, credit_id, account_id, amount):
        credit_repay = RepayCreditRequest(creditId=credit_id, accountId=account_id, amount=amount)
        response = ValidatedCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.REPAY_CREDIT,
            ResponseSpecs.request_ok()
        ).post(credit_repay)
        return response

    def invalid_credit_repay(self, create_user_request: CreateUserRequest, credit_id, account_id, amount):
        credit_repay = RepayCreditRequest(creditId=credit_id, accountId=account_id, amount=amount)
        response = CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.REPAY_CREDIT,
            ResponseSpecs.request_unprocessable()
        ).post(credit_repay)
        return response
