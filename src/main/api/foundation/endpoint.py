from dataclasses import dataclass
from enum import Enum
from typing import Optional, Type

from src.main.api.models.base_model import BaseModel
from src.main.api.models.requests.create_user_request import CreateUserRequest
from src.main.api.models.requests.deposit_request import DepositRequest
from src.main.api.models.requests.login_user_request import LoginUserRequest
from src.main.api.models.requests.repay_credit_request import RepayCreditRequest
from src.main.api.models.requests.request_credit_request import RequestCreditRequest
from src.main.api.models.requests.transfer_request import TransferRequest
from src.main.api.models.responses.create_account_response import CreateAccountResponse
from src.main.api.models.responses.create_user_response import CreateUserResponse
from src.main.api.models.responses.deposit_response import DepositResponse
from src.main.api.models.responses.login_user_response import LoginUserResponse
from src.main.api.models.responses.repay_credit_response import RepayCreditResponse
from src.main.api.models.responses.request_credit_response import RequestCreditResponse
from src.main.api.models.responses.transfer_response import TransferResponse


@dataclass
class EndpointConfiguration:
    url: str
    request_model: Optional[Type[BaseModel]]
    response_model: Optional[Type[BaseModel]]


class Endpoint(Enum):
    ADMIN_CREATE_USER = EndpointConfiguration(
        request_model=CreateUserRequest,
        url="/admin/create",
        response_model=CreateUserResponse
    )

    ADMIN_DELETE_USER = EndpointConfiguration(
        request_model=None,
        url="/admin/users",
        response_model=None
    )

    LOGIN_USER = EndpointConfiguration(
        request_model=LoginUserRequest,
        url="/auth/token/login",
        response_model=LoginUserResponse
    )

    ACCOUNT_CREATE = EndpointConfiguration(
        request_model=None,
        url="/account/create",
        response_model=CreateAccountResponse
    )

    ACCOUNT_DEPOSIT = EndpointConfiguration(
        request_model=DepositRequest,
        url="/account/deposit",
        response_model=DepositResponse
    )

    ACCOUNT_TRANSFER = EndpointConfiguration(
        request_model=TransferRequest,
        url="/account/transfer",
        response_model=TransferResponse
    )

    REQUEST_CREDIT = EndpointConfiguration(
        request_model=RequestCreditRequest,
        url="/credit/request",
        response_model=RequestCreditResponse
    )

    REPAY_CREDIT = EndpointConfiguration(
        request_model=RepayCreditRequest,
        url="/credit/repay",
        response_model=RepayCreditResponse
    )
