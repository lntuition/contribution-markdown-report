from unittest.mock import MagicMock, patch

import pytest

from request import RequestException, fetch_raw_text


@patch("requests.get")
def test_fetch_raw_test_success(mock_request_get):
    test_text = "test_text"
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = test_text
    mock_request_get.return_value = mock_response

    assert fetch_raw_text(url="url") == test_text


@patch("requests.get")
def test_fetch_raw_test_fail(mock_request_get):
    test_text = "test_text"
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.text = test_text
    mock_request_get.return_value = mock_response

    with pytest.raises(RequestException):
        fetch_raw_text(url="url")
