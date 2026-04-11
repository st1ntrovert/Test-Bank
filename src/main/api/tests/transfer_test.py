import requests


class TestTransfer:
    def test_transfer(self):
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
        admin_token = login_admin_response.json().get("token")

        create_first_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": "MaximFirst111",
                "password": "Pas!sw0rd",
                "role": "ROLE_USER"
            },
            headers={
                "accept": "application/json",
                "Content-type": "application/json",
                "Authorization": f"Bearer {admin_token}"
            }
        )

        assert create_first_user_response.status_code == 200
        assert create_first_user_response.json().get("username") == "MaximFirst111"
        assert create_first_user_response.json().get("role") == "ROLE_USER"

        create_second_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": "MaximSecond222",
                "password": "Pas!sw0rd",
                "role": "ROLE_USER"
            },
            headers={
                "accept": "application/json",
                "Content-type": "application/json",
                "Authorization": f"Bearer {admin_token}"
            }
        )

        assert create_second_user_response.status_code == 200
        assert create_second_user_response.json().get("username") == "MaximSecond222"
        assert create_second_user_response.json().get("role") == "ROLE_USER"

        login_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "MaximSecond222",
                "password": "Pas!sw0rd"
            },
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            }
        )

        assert login_user_response.status_code == 200
        second_user_token = login_user_response.json().get("token")

        create_account_response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {second_user_token}"
            }
        )

        assert create_account_response.status_code == 201
        assert create_account_response.json().get("balance") == 0
        second_account_id = create_account_response.json().get("id")

        login_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "MaximFirst111",
                "password": "Pas!sw0rd"
            },
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            }
        )

        assert login_user_response.status_code == 200
        first_user_token = login_user_response.json().get("token")

        create_account_response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {first_user_token}"
            }
        )

        assert create_account_response.status_code == 201
        assert create_account_response.json().get("balance") == 0
        first_account_id = create_account_response.json().get("id")

        deposit_response = requests.post(
            url="http://localhost:4111/api/account/deposit",
            json={
                "accountId": first_account_id,
                "amount": 5000
            },
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {first_user_token}"
            }
        )

        assert deposit_response.status_code == 200
        assert deposit_response.json().get("balance") == 5000

        transfer_response = requests.post(
            url="http://localhost:4111/api/account/transfer",
            json={
                "fromAccountId": first_account_id,
                "toAccountId": second_account_id,
                "amount": 3000
            },
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {first_user_token}",
                "Content-Type": "application/json"
            }
        )

        assert transfer_response.status_code == 200
        assert transfer_response.json().get("fromAccountIdBalance") == 2000

        transactions_response = requests.get(
            url=f"http://localhost:4111/api/account/transactions/{second_account_id}",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {second_user_token}"
            }
        )

        assert transactions_response.status_code == 200
        transactions = transactions_response.json().get("transactions")
        assert any(t.get("type") == "transfer_in" and t.get("amount") == 3000 for t in transactions)
        assert transactions_response.json().get("balance") == 3000

    def test_transfer_invalid_amount(self):
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
        admin_token = login_admin_response.json().get("token")

        create_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": "MaxInvalid2",
                "password": "Pas!sw0rd",
                "role": "ROLE_USER"},
            headers={
                "accept": "application/json",
                "Content-type": "application/json",
                "Authorization": f"Bearer {admin_token}"
            }
        )
        assert create_user_response.status_code == 200

        login_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "MaxInvalid2",
                "password": "Pas!sw0rd"
            },
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            }
        )
        assert login_user_response.status_code == 200
        token = login_user_response.json().get("token")

        account1 = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        assert account1.status_code == 201
        account1_id = account1.json().get("id")

        account2 = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        assert account2.status_code == 201
        account2_id = account2.json().get("id")

        deposit_response = requests.post(
            url="http://localhost:4111/api/account/deposit",
            json={
                "accountId": account1_id,
                "amount": 5000
            },
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        assert deposit_response.status_code == 200

        transfer_response = requests.post(
            url="http://localhost:4111/api/account/transfer",
            json={
                "fromAccountId": account1_id,
                "toAccountId": account2_id,
                "amount": 499
            },
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert transfer_response.status_code == 400
