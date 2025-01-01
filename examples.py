# example_usage.py

from mpesa_sdk import MPesaSDK, MPesaError

# Example Usage
if __name__ == "__main__":
    consumer_key = "JYGkB3WfnM3LbcPdg8IFL4Qwa0MSDlHEHS7hHAfjvzacKZGk"
    consumer_secret = "TUkkw5FRJJX3UNGz6pFXGPKakjXB7H3Miv94zneNrMDTF8wdrGtA4Lo1frGC0D9F"
    sdk = MPesaSDK(consumer_key, consumer_secret, environment='sandbox')

    try:
        sdk.authenticate()

        # STK Push
        stk_push_response = sdk.stk_push(
            merchant_request_id="SFC-Testing-9146-4216-9455-e3947ac570fc",
            business_short_code="554433",
            password="123",
            timestamp="20160216165627",
            transaction_type="CustomerPayBillOnline",
            amount="10.00",
            party_a="251700404789",
            party_b="554433",
            phone_number="251700404789",
            transaction_desc="Monthly Unlimited Package via Chatbot",
            callback_url="https://apigee-listener.oat.mpesa.safaricomet.net/api/ussd-push/result",
            account_reference="DATA",
            reference_data=[
                {
                    "Key": "BundleName",
                    "Value": "Monthly Unlimited Bundle"
                },
                {
                    "Key": "BundleType",
                    "Value": "Self"
                },
                {
                    "Key": "TINNumber",
                    "Value": "89234093223"
                }
            ]
        )
        print("STK Push Response:", stk_push_response)

        # C2B Register URL
        c2b_register_response = sdk.c2b_register_url(
            short_code="802000",
            response_type="Completed",
            confirmation_url="https://www.myservice:8080/confirmation",
            validation_url="https://www.myservice:8080/validation"
        )
        print("C2B Register URL Response:", c2b_register_response)

        # C2B Simulate
        c2b_simulate_response = sdk.c2b_payment(
            request_ref_id="unique_request_ref_id",
            command_id="CustomerPayBillOnline",
            remark="Payment for services",
            channel_session_id="10100000037656400042",
            source_system="USSD",
            timestamp="20250101123456",
            parameters=[
                {"Key": "Amount", "Value": "500"},
                {"Key": "AccountReference", "Value": "TU781RE"},
                {"Key": "Currency", "Value": "ETB"}
            ],
            reference_data=[
                {"Key": "AppVersion", "Value": "v0.2"}
            ],
            initiator={
                "IdentifierType": 1,
                "Identifier": "251799100026",
                "SecurityCredential": "your_security_credential",
                "SecretKey": "your_secret_key"
            },
            primary_party={
                "IdentifierType": 1,
                "Identifier": "251799100026"
            },
            receiver_party={
                "IdentifierType": 4,
                "Identifier": "370360",
                "ShortCode": "370360"
            }
        )
        print("C2B Simulate Response:", c2b_simulate_response)

        # B2C Payment
        b2c_response = sdk.b2c_payment_request(
            initiator_name="testapiuser",
            security_credential="aoudnoai",
            command_id="BusinessPayment",
            occasion="StallOwner",
            amount=100,
            party_a="600000",
            party_b="251711959143",
            remarks="Test B2C",
            queue_timeout_url="https://www.myservice:8080/b2c/result",
            result_url="https://www.myservice:8080/b2c/result"
        )
        print("B2C Payment Response:", b2c_response)

        
    except MPesaError as e:
        print(f"Error: {str(e)}")
