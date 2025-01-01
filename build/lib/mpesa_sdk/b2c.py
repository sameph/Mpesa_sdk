import requests
from .exceptions import APIRequestError

class B2C:
    def __init__(self, access_token, base_url):
        self.access_token = access_token
        self.base_url = base_url

    def payment_request(self, initiator_name, security_credential, command_id, occasion, amount, party_a, party_b, remarks, queue_timeout_url, result_url):
        url = f"{self.base_url}/mpesa/b2c/v2/paymentrequest"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "InitiatorName": initiator_name,
            "SecurityCredential": security_credential,
            "CommandID": command_id,
            "Occasion": occasion,
            "Amount": amount,
            "PartyA": party_a,
            "PartyB": party_b,
            "Remarks": remarks,
            "QueueTimeOutURL": queue_timeout_url,
            "ResultURL": result_url
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            raise APIRequestError(f"B2C Payment Request failed: {response.text}")
