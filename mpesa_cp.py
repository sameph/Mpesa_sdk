import datetime
import base64
import requests
from requests.auth import HTTPBasicAuth

class API:
    """Kenya MPESA SDK Implementation."""

    def __init__(self, env="sandbox", app_key=None, app_secret=None):
        """
        Initialize API client.

        :param env: The environment to use, either "sandbox" or "production".
        :param app_key: The application key for authentication.
        :param app_secret: The application secret for authentication.
        """
        if env not in ["sandbox", "production"]:
            raise ValueError("Invalid environment. Choose 'sandbox' or 'production'.")
        self.env = env
        self.app_key = app_key
        self.app_secret = app_secret
        self.base_url = (
            "https://apisandbox.safaricom.et" if env == "sandbox" else "https://api.safaricom.et"
        )

    def _get_headers(self):
        """Generate headers for API requests."""
        return {
            "Authorization": f"Bearer {self.authentication_token}",
            "Content-Type": "application/json",
        }

    @property
    def authentication_token(self):
        """Return an authentication token."""
        return self.authenticate()

    def authenticate(self):
        """
        Authenticate and retrieve access token.

        :return: Access token as a string.
        """
        url = f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials"
        try:
            response = requests.get(url, auth=HTTPBasicAuth(self.app_key, self.app_secret))
            response.raise_for_status()
            return response.json().get("access_token")
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to authenticate: {e}")

    def _post_request(self, endpoint, payload):
        """
        Make a POST request.

        :param endpoint: API endpoint to call.
        :param payload: Data payload for the POST request.
        :return: Response JSON.
        """
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise RuntimeError(f"API request failed: {e}")

    def b2c(self, initiator_name, security_credential, command_id, amount, party_a, party_b, remarks, queue_timeout_url, result_url, occasion=None):
        """
        Perform a B2C payment request.

        :param initiator_name: Name of the initiator.
        :param security_credential: Security credential for the request.
        :param command_id: Type of transaction command.
        :param amount: Payment amount.
        :param party_a: Source of funds.
        :param party_b: Recipient of funds.
        :param remarks: Transaction remarks.
        :param queue_timeout_url: URL to call in case of timeout.
        :param result_url: URL to send the transaction result.
        :param occasion: Additional information.
        :return: Response JSON.
        """
        payload = {
            "InitiatorName": initiator_name,
            "SecurityCredential": security_credential,
            "CommandID": command_id,
            "Amount": amount,
            "PartyA": party_a,
            "PartyB": party_b,
            "Remarks": remarks,
            "QueueTimeOutURL": queue_timeout_url,
            "ResultURL": result_url,
            "Occasion": occasion,
        }
        return self._post_request("/mpesa/b2c/v1/paymentrequest", payload)

    def c2b_register_url(self, shortcode, response_type, confirmation_url, validation_url):
        """
        Register URLs for C2B transactions.

        :param shortcode: Short code for the business.
        :param response_type: Expected response type (e.g., "Completed").
        :param confirmation_url: URL for confirmation.
        :param validation_url: URL for validation.
        :return: Response JSON.
        """
        payload = {
            "ShortCode": shortcode,
            "ResponseType": response_type,
            "ConfirmationURL": confirmation_url,
            "ValidationURL": validation_url,
        }
        return self._post_request("/mpesa/c2b/v1/registerurl", payload)

    def c2b_simulate(self, shortcode, command_id, amount, msisdn, bill_ref_number):
        """
        Simulate a C2B transaction.

        :param shortcode: Short code for the business.
        :param command_id: Type of transaction command.
        :param amount: Transaction amount.
        :param msisdn: Mobile number initiating the transaction.
        :param bill_ref_number: Bill reference number.
        :return: Response JSON.
        """
        payload = {
            "ShortCode": shortcode,
            "CommandID": command_id,
            "Amount": amount,
            "Msisdn": msisdn,
            "BillRefNumber": bill_ref_number,
        }
        return self._post_request("/mpesa/c2b/v1/simulate", payload)

    def stkpush(self, business_shortcode, passcode, amount, callback_url, reference_code, phone_number, description):
        """
        Initiate STK Push transaction.

        :param business_shortcode: Business short code.
        :param passcode: Security passcode.
        :param amount: Transaction amount.
        :param callback_url: URL for transaction callback.
        :param reference_code: Account reference.
        :param phone_number: Customer's phone number.
        :param description: Transaction description.
        :return: Response JSON.
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        password = f"{business_shortcode}{passcode}{timestamp}"
        encoded_password = base64.b64encode(password.encode()).decode("utf-8")

        payload = {
            "BusinessShortCode": business_shortcode,
            "Password": encoded_password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": business_shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": callback_url,
            "AccountReference": reference_code,
            "TransactionDesc": description,
        }
        return self._post_request("/mpesa/stkpush/v1/processrequest", payload)
if __name__ == "__main__":
    api_client = API(env="sandbox", app_key="JYGkB3WfnM3LbcPdg8IFL4Qwa0MSDlHEHS7hHAfjvzacKZGk", app_secret="TUkkw5FRJJX3UNGz6pFXGPKakjXB7H3Miv94zneNrMDTF8wdrGtA4Lo1frGC0D9F")

    try:
        # Authenticate and fetch token
        print("Authenticating...")
        token = api_client.authentication_token
        print(f"Access Token: {token}")

        # Perform a B2C payment
        response = api_client.b2c(
            initiator_name="testapi",
            security_credential="YourSecurityCredential",
            command_id="BusinessPayment",
            amount="1000",
            party_a="600000",
            party_b="254700000000",
            remarks="Test Transaction",
            queue_timeout_url="https://example.com/timeout",
            result_url="https://example.com/result"
        )
        print("B2C Response:", response)
    except Exception as e:
        print(f"Error: {e}")
