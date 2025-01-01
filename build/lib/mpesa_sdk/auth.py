import base64
import requests
from .exceptions import AuthenticationError

class MPesaSDK:
    """MPesa SDK for interacting with Safaricom APIs."""

    def __init__(self, consumer_key, consumer_secret, environment='sandbox'):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.environment = environment
        self.base_url = self._get_base_url()
        self.access_token = None

    def _get_base_url(self):
        if self.environment == 'sandbox':
            return "https://apisandbox.safaricom.et"
        elif self.environment == 'production':
            return "https://api.safaricom.co.et"
        else:
            raise ValueError("Invalid environment. Choose 'sandbox' or 'production'.")

    def authenticate(self):
        url = f"{self.base_url}/v1/token/generate?grant_type=client_credentials"
        credentials = f"{self.consumer_key}:{self.consumer_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        headers = {"Authorization": f"Basic {encoded_credentials}"}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            self.access_token = data['access_token']
            print("Authentication successful.")
        else:
            raise AuthenticationError(f"Authentication failed: {response.text}")
