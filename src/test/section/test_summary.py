import pytest

from lib.section.summary import SummaryGenerator
from test.section.test_base import mock_language_setting, mock_data


def test_summary_process(mock_data, mock_language_setting):
    summary = SummaryGenerator(
        data=mock_data(
            [0, 1, 2, 3]
        ),
        setting=mock_language_setting,
    )

    summary.process(config={})

    mock_language_setting.format_summary.assert_called()
