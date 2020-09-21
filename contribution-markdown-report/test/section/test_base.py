from typing import List
from unittest.mock import MagicMock

import pandas as pd
import pytest

from language.base import LanguageSetting


class SkeletonLanguageSetting(LanguageSetting):
    def header_greeting(self, username: str) -> str:
        return ""

    def header_notice(self, repo_url: str, issue_url: str) -> str:
        return ""

    def summary_title(self) -> str:
        return ""

    def summary_today(self, today: str, length: str, count: str) -> str:
        return ""

    def summary_maximum(self, date: str, count: str) -> str:
        return ""

    def summary_total(self, sum: str, avg: str) -> str:
        return ""

    def summary_peak(self, length: str, start: str, end: str) -> str:
        return ""

    def summary_cur_peak(self, length: str, start: str) -> str:
        return ""

    def graph_title(self) -> str:
        return ""

    def graph_dayofweek_label(self) -> List[str]:
        return ["0", "1", "2", "3", "4", "5", "6"]

    def graph_contribution_axis(self) -> str:
        return ""

    def graph_day_axis(self) -> str:
        return ""

    def graph_dayofweek_axis(self) -> str:
        return ""

    def graph_month_axis(self) -> str:
        return ""

    def graph_count_sum_recent_title(self) -> str:
        return ""

    def graph_count_sum_full_title(self) -> str:
        return ""

    def graph_dayofweek_sum_recent_title(self) -> str:
        return ""

    def graph_dayofweek_mean_full_title(self) -> str:
        return ""

    def graph_month_sum_recent_title(self) -> str:
        return ""

    def graph_month_mean_full_title(self) -> str:
        return ""


@pytest.fixture(scope="module")
def mock_language_setting():
    return MagicMock(wrap=SkeletonLanguageSetting)


def mock_data(count, start, finish):
    return pd.DataFrame(
        {
            "count": count,
            "date": pd.date_range(start, finish),
        }
    )
