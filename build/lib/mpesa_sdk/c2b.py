import requests
from .exceptions import APIRequestError

class C2B:
    def __init__(self, access_token, base_url):
        self.access_token = access_token
        self.base_url = base_url

    def register_url(self, short_code, response_type, confirmation_url, validation_url):
        url = f"{self.base_url}/v1/c2b-register-url/register?apikey={self.consumer_key}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "ShortCode": short_code,
            "ResponseType": response_type,
            "CommandID": "RegisterURL",
            "ConfirmationURL": confirmation_url,
            "ValidationURL": validation_url
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            raise APIRequestError(f"C2B Register URL failed: {response.text}")

    def payment(self, request_ref_id, command_id, remark, channel_session_id, source_system, timestamp, parameters, reference_data, initiator, primary_party, receiver_party):
        url = f"{self.base_url}/v1/c2b/payments"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "RequestRefID": request_ref_id,
            "CommandID": command_id,
            "Remark": remark,
            "ChannelSessionID": channel_session_id,
            "SourceSystem": source_system,
            "Timestamp": timestamp,
            "Parameters": parameters,
            "ReferenceData": reference_data,
            "Initiator": initiator,
            "PrimaryParty": primary_party,
            "ReceiverParty": receiver_party
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            raise APIRequestError(f"C2B Payment failed: {response.text}")
