from unittest.mock import patch

import pytest


class FakeResponse:
    def __init__(self, status_code: int, text: str) -> None:
        self.__status_code = status_code
        self.__text = text

    @property
    def status_code(self) -> int:
        return self.__status_code

    @property
    def text(self) -> str:
        return self.__text


class FakeRequest:
    @staticmethod
    def get(url: str) -> FakeResponse:
        text = "text"

        if url == "200":
            status_code = 200
        elif url == "404":
            status_code = 404

        return FakeResponse(status_code=status_code, text=text)


@pytest.fixture
def use_fake_request():
    with patch("requests.get", wraps=FakeRequest.get):
        yield
