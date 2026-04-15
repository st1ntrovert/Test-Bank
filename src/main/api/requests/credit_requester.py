from http import HTTPStatus

import requests
from requests import Response

from src.main.api.models.requests.request_credit_request import RequestCreditRequest
from src.main.api.models.responses.request_credit_response import RequestCreditResponse
from src.main.api.requests.requester import Requester


class CreditRequester(Requester):
    def post(self, credit_request: RequestCreditRequest) -> RequestCreditResponse | Response:
        url = f"{self.base_url}/credit/request"
        response = requests.post(
            url=url,
            json=credit_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)

        if response.status_code == HTTPStatus.CREATED:
            return RequestCreditResponse(**response.json())
        return response
