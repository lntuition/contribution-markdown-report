from pathlib import Path
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse

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
        parts = urlparse(url)
        qs = parse_qs(parts.query)

        # Request test
        if "status" in qs:
            status_code = int(qs["status"][0])
            return FakeResponse(status_code=status_code, text="text")

        # Crawler test
        if "from" in qs:
            snapshot_file = f"{qs['from'][0][:4]}_snapshot.html"
            snapshot_path = Path(__file__).absolute().parents[1].joinpath("asset", snapshot_file)
            with open(snapshot_path, "r") as snapshot:
                text = snapshot.read()
                return FakeResponse(status_code=200, text=text)


@pytest.fixture
def use_fake_request():
    with patch("requests.get", wraps=FakeRequest.get):
        yield
