import pytest

from lib.section.header import HeaderGenerator
from test.section.test_base import mock_language_setting


@pytest.fixture()
def username():
    return "lntuition"


def test_header_configure(username, mock_language_setting):
    header = HeaderGenerator(
        username=username,
        setting=mock_language_setting
    )

    config = header.configure()
    assert config["username"] == username


def test_header_process(mock_language_setting):
    header = HeaderGenerator(
        username=username,
        setting=mock_language_setting
    )

    header.process(config={})

    mock_language_setting.format_header.assert_called()
