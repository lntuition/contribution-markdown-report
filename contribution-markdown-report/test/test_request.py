from unittest.mock import MagicMock, patch

import pytest

from request import Request, RequestException


@patch("requests.get")
def test_fetch_success(mock_request_get):
    test_text = "test_text"
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = test_text
    mock_request_get.return_value = mock_response

    assert Request.fetch(url="url") == test_text


@patch("requests.get")
def test_fetch_fail(mock_request_get):
    test_text = "test_text"
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.text = test_text
    mock_request_get.return_value = mock_response

    with pytest.raises(RequestException):
        Request.fetch(url="url")
