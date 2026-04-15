from http import HTTPStatus

import requests
from requests import Response

from src.main.api.models.requests.repay_credit_request import RepayCreditRequest
from src.main.api.models.responses.repay_credit_response import RepayCreditResponse
from src.main.api.requests.requester import Requester


class CreditRepayRequester(Requester):
    def post(self, repay_credit_request: RepayCreditRequest) -> RepayCreditResponse | Response:
        url = f"{self.base_url}/credit/repay"
        response = requests.post(
            url=url,
            json=repay_credit_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)

        if response.status_code == HTTPStatus.OK:
            return RepayCreditResponse(**response.json())
        return response
