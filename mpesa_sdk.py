import base64
import requests

class MPesaError(Exception):
    """Base class for MPesa SDK errors."""
    pass

class AuthenticationError(MPesaError):
    """Raised when authentication fails."""
    pass

class APIRequestError(MPesaError):
    """Raised when an API request fails."""
    pass

class MPesaSDK:
    """MPesa SDK for interacting with Safaricom APIs."""

    def __init__(self, consumer_key, consumer_secret, environment='sandbox'):
        """
        Initialize the MPesa SDK.

        Args:
            consumer_key (str): The consumer key provided by Safaricom.
            consumer_secret (str): The consumer secret provided by Safaricom.
            environment (str): Either 'sandbox' or 'production'.
        """
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.environment = environment
        self.base_url = self._get_base_url()
        self.access_token = None

    def _get_base_url(self):
        """Get the base URL for the API."""
        if self.environment == 'sandbox':
            return "https://apisandbox.safaricom.et"
        elif self.environment == 'production':
            return "https://api.safaricom.co.et"
        else:
            raise ValueError("Invalid environment. Choose 'sandbox' or 'production'.")

    def authenticate(self):
        """
        Authenticate with the Safaricom API to get an access token.
        Raises:
            AuthenticationError: If authentication fails.
        """
        url = f"{self.base_url}/v1/token/generate?grant_type=client_credentials"
        credentials = f"{self.consumer_key}:{self.consumer_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        print(encoded_credentials)
        headers = {
            "Authorization": f"Basic {encoded_credentials}"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            self.access_token = data['access_token']
            print("Authentication successful.")
        else:
            raise AuthenticationError(f"Authentication failed: {response.text}")

    def stk_push(self, merchant_request_id, business_short_code, password, timestamp, transaction_type, amount, party_a, party_b, phone_number, callback_url, account_reference, transaction_desc, reference_data):
        """
        Initiate an STK Push.

        Args:
            merchant_request_id (str): Unique ID for the request.
            business_short_code (str): Short code of the business.
            password (str): Base64 encoded string combining short code, passkey, and timestamp.
            timestamp (str): Timestamp of the request.
            transaction_type (str): Type of transaction, e.g., "CustomerPayBillOnline".
            amount (float): Amount to be transacted.
            party_a (str): Phone number sending the money.
            party_b (str): Business short code receiving the money.
            phone_number (str): Phone number sending the money.
            callback_url (str): URL to receive the callback.
            account_reference (str): Account reference for the transaction.
            transaction_desc (str): Description of the transaction.
            reference_data (dict): Additional reference data.

        Returns:
            dict: API response.
        """
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

    def c2b_register_url(self, short_code, response_type, confirmation_url, validation_url):
        """
        Register C2B URLs.

        Args:
            short_code (str): The business short code.
            response_type (str): "Completed" or "Cancelled".
            confirmation_url (str): URL for payment confirmations.
            validation_url (str): URL for payment validations.

        Returns:
            dict: API response.
        """
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

    def c2b_payment(self, request_ref_id, command_id, remark, channel_session_id, source_system, timestamp, parameters, reference_data, initiator, primary_party, receiver_party):
        """
        Process a C2B payment.

        Args:
            request_ref_id (str): The unique request reference ID.
            command_id (str): Transaction type, e.g., "CustomerPayBillOnline."
            remark (str): Transaction remark.
            channel_session_id (str): Unique session ID.
            source_system (str): Source system of the transaction.
            timestamp (str): Timestamp of the transaction.
            parameters (list): List of key-value pairs for transaction parameters.
            reference_data (list): List of key-value pairs for reference data.
            initiator (dict): Initiator information.
            primary_party (dict): Primary party information.
            receiver_party (dict): Receiver party information.

        Returns:
            dict: API response.
        """
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

    def b2c_payment_request(self, initiator_name, security_credential, command_id, amount, party_a, party_b, remarks, queue_timeout_url, result_url, occasion):
        """
        Make a B2C payment request.

        Args:
            initiator_name (str): Initiator username.
            security_credential (str): Base64 encoded security credential.
            command_id (str): Transaction type, e.g., "BusinessPayment".
            occasion (str): Occasion for the payment.
            amount (float): Amount to be sent.
            party_a (str): Organization short code initiating the payment.
            party_b (str): Customer phone number (format: 251...).
            remarks (str): Payment remarks.
            queue_timeout_url (str): URL for timeout response.
            result_url (str): URL for transaction result.

        Returns:
            dict: API response.
        """
        url = f"{self.base_url}/mpesa/b2c/v1/paymentrequest"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "InitiatorName": initiator_name,
            "SecurityCredential": security_credential,
            "Occasion": occasion,
            "CommandID": command_id,
            "PartyA": party_a,
            "PartyB": party_b,
            "Remarks": remarks,
            "Amount": amount,
            "QueueTimeOutURL": queue_timeout_url,
            "ResultURL": result_url
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            raise APIRequestError(f"B2C Payment Request failed: {response.text}")


