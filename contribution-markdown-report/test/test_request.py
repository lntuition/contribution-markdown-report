import pytest

from request import Request, RequestException


def test_fetch_success(use_fake_request):
    assert Request.fetch(url="200") == "text"


def test_fetch_fail(use_fake_request):
    with pytest.raises(RequestException):
        Request.fetch(url="404")
