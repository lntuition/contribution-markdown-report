from lib.section.summary import SummaryGenerator
from test.section.test_base import mock_language_setting, mock_data


def test_summary_generate(mock_data, mock_language_setting):
    summary = SummaryGenerator(
        data=mock_data(
            [0, 1, 2, 3]
        ),
        setting=mock_language_setting,
    )

    summary.generate()

    mock_language_setting.format_summary.assert_called_with(
        today=summary.today_configure(),
        maximum=summary.max_configure(),
        total=summary.total_configure(),
        continuous=summary.continuous_configure(),
    )
