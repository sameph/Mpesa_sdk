import requests
from ..mpesa_sdk import APIRequestError

class STKPush:
    def __init__(self, access_token, base_url):
        self.access_token = access_token
        self.base_url = base_url

    def stk_push(self, merchant_request_id, business_short_code, password, timestamp, transaction_type, amount, party_a, party_b, phone_number, callback_url, account_reference, transaction_desc, reference_data):
        url = f"{self.base_url}/mpesa/stkpush/v3/processrequest"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "MerchantRequestID": merchant_request_id,
            "BusinessShortCode": business_short_code,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": transaction_type,
            "Amount": amount,
            "PartyA": party_a,
            "PartyB": party_b,
            "PhoneNumber": phone_number,
            "CallBackURL": callback_url,
            "AccountReference": account_reference,
            "TransactionDesc": transaction_desc,
            "ReferenceData": reference_data
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            raise APIRequestError(f"STK Push request failed: {response.text}")
