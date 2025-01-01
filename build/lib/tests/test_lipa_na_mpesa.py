import responses
from sdk.client import MpesaClient

@responses.activate
def test_lipa_na_mpesa():
    responses.add(
        responses.POST,
        "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
        json={"ResponseCode": "0", "ResponseDescription": "Success"},
        status=200,
    )

    client = MpesaClient(api_key="sandbox_key", api_secret="sandbox_secret")
    response = client.lipa_na_mpesa(
        phone_number="254712345678",
        amount=10,
        account_reference="Test",
        transaction_desc="Payment Test",
        callback_url="https://your-callback-url.com",
    )

    assert response["ResponseCode"] == "0"
