import pytest
from sdk.client import MpesaClient

@pytest.fixture
def client():
    return MpesaClient(api_key="test_key", api_secret="test_secret")

def test_generate_token(client, mocker):
    mock_response = mocker.patch("requests.get")
    mock_response.return_value.status_code = 200
    mock_response.return_value.json.return_value = {
        "access_token": "test_token",
        "expires_in": 3600,
    }

    token = client.generate_token()
    assert token == "test_token"
    assert mock_response.called
