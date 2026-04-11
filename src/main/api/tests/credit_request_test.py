import requests


class TestCreditRequest:
    def test_credit_request_valid(self):
        login_admin_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "admin",
                "password": "123456"
            },
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            }
        )

        assert login_admin_response.status_code == 200
        token = login_admin_response.json().get("token")

        create_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": "Max123455",
                "password": "Pas!sw0rd",
                "role": "ROLE_CREDIT_SECRET"
            },
            headers={
                "accept": "application/json",
                "Content-type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_user_response.status_code == 200
        assert create_user_response.json().get("username") == "Max123455"
        assert create_user_response.json().get("role") == "ROLE_CREDIT_SECRET"

        login_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "Max123455",
                "password": "Pas!sw0rd"
            },
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            }
        )

        assert login_user_response.status_code == 200
        token = login_user_response.json().get("token")

        create_account_response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_account_response.status_code == 201
        assert create_account_response.json().get("balance") == 0
        account_id = create_account_response.json().get("id")

        credit_request_response = requests.post(
            url="http://localhost:4111/api/credit/request",
            json={
                "accountId": account_id,
                "amount": 5000,
                "termMonths": 12
            },
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert credit_request_response.status_code == 201
        assert credit_request_response.json().get("balance") == 5000
        assert credit_request_response.json().get("termMonths") == 12


    def test_credit_request_user_forbidden(self):
        login_admin_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "admin",
                "password": "123456"
            },
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            }
        )

        assert login_admin_response.status_code == 200
        token = login_admin_response.json().get("token")

        create_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": "MaxNotCredit",
                "password": "Pas!sw0rd",
                "role": "ROLE_USER"
            },
            headers={
                "accept": "application/json",
                "Content-type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_user_response.status_code == 200
        assert create_user_response.json().get("username") == "MaxNotCredit"
        assert create_user_response.json().get("role") == "ROLE_USER"

        login_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "MaxNotCredit",
                "password": "Pas!sw0rd"
            },
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            }
        )

        assert login_user_response.status_code == 200
        token = login_user_response.json().get("token")

        create_account_response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_account_response.status_code == 201
        assert create_account_response.json().get("balance") == 0
        account_id = create_account_response.json().get("id")

        credit_request_response = requests.post(
            url="http://localhost:4111/api/credit/request",
            json={
                "accountId": account_id,
                "amount": 5000,
                "termMonths": 12
            },
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert credit_request_response.status_code == 403