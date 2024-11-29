import pytest
from api_client.api.default_api import DefaultApi
from api_client import ApiClient, Configuration

# Initialisiere den API-Client
@pytest.fixture
def api_client():
    config = Configuration()
    config.host = "http://localhost:4000"  # API-Base-URL
    return DefaultApi(ApiClient(config))

def test_get_users(api_client):
    # Ruf den API-Endpunkt auf
    response = api_client.get_users_with_http_info()
    data, status, headers = response

    # Überprüfe den Statuscode
    assert status == 200

    # Überprüfe die Antwortdaten
    assert isinstance(data, list)  # Erwartet eine Liste
    for user in data:
        assert "id" in user
        assert "name" in user

def test_invalid_endpoint(api_client):
    # Test für einen ungültigen Endpunkt
    with pytest.raises(Exception):
        api_client.non_existing_endpoint()