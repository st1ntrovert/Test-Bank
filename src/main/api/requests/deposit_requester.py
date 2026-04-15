from http import HTTPStatus

import requests
from requests import Response

from src.main.api.models.requests.deposit_request import DepositRequest
from src.main.api.models.responses.deposit_response import DepositResponse
from src.main.api.requests.requester import Requester


class DepositRequester(Requester):
    def post(self, deposit_request: DepositRequest) -> DepositResponse | Response:
        url = f"{self.base_url}/account/deposit"
        response = requests.post(
            url=url,
            json=deposit_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)

        if response.status_code == HTTPStatus.OK:
            return DepositResponse(**response.json())
        return response
