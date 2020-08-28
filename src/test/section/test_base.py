import pytest

from unittest.mock import MagicMock

from lib.base.type import ConfigType
from lib.language.base import BaseLanguageSetting


class SkeletonLanguageSetting(BaseLanguageSetting):
    def format_header(self, config: ConfigType) -> str:
        return ""

    def format_summary(self, config: ConfigType) -> str:
        return ""

    def config_graph(self) -> ConfigType:
        return {

        }


@pytest.fixture(scope="module")
def mock_language_setting():
    return MagicMock(wrap=SkeletonLanguageSetting)
