from http import HTTPStatus

import requests

from src.main.api.models.requests.transfer_request import TransferRequest
from src.main.api.models.responses.transfer_response import TransferResponse
from src.main.api.requests.requester import Requester


class TransferRequester(Requester):
    def post(self, transfer_request: TransferRequest):
        url = f"{self.base_url}/account/transfer"
        response = requests.post(
            url=url,
            json=transfer_request.model_dump(),
            headers=self.headers,
        )
        self.response_spec(response)

        if response.status_code == HTTPStatus.OK:
            return TransferResponse(**response.json())
        return response
