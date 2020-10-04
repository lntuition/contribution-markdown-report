import pytest

from request import Request, RequestException


def test_fetch_success(use_fake_request: None) -> None:
    assert Request.fetch(url="https://test.request.com?status=200") == "text"


def test_fetch_fail(use_fake_request: None) -> None:
    with pytest.raises(RequestException):
        Request.fetch(url="https://test.request.com?status=404")
