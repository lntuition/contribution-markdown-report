import pandas as pd
import pytest

from unittest.mock import MagicMock

from lib.base.type import ConfigType
from lib.language.base import LanguageSetting


class SkeletonLanguageSetting(LanguageSetting):
    def format_header(self, username: str) -> str:
        return ""

    def format_summary(
        self, today: ConfigType, maximum: ConfigType, total: ConfigType, continuous: ConfigType
    ) -> str:
        return ""

    def config_graph(self) -> ConfigType:
        return {

        }


@pytest.fixture(scope="module")
def mock_language_setting():
    return MagicMock(wrap=SkeletonLanguageSetting)


@pytest.fixture()
def mock_data():
    def _mock_data(count):
        return pd.DataFrame({
            "count": count,
            "date": pd.date_range("2013-01-01", periods=len(count)),
        })

    return _mock_data
