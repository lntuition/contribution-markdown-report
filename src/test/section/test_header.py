from lib.section.header import HeaderGenerator
from test.section.test_base import mock_language_setting


def test_header_generate(mock_language_setting):
    username = "lntuition"
    header = HeaderGenerator(
        username=username,
        setting=mock_language_setting
    )

    header.generate()

    mock_language_setting.format_header.assert_called_with(
        username=username
    )
