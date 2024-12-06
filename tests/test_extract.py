import pytest
from app.extract import extract_data

def test_extract_data_from_api(mocker):
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"key": "value"}
    mocker.patch("requests.get", return_value=mock_response)
    
    data = extract_data(
        source_type="api",
        connection_details={"headers": {"Authorization": "Bearer YOUR_API_KEY"}},
        query_or_endpoint="https://api.example.com/data"
    )
    
    assert data == {"key": "value"}