from abc import ABCMeta, abstractmethod

from lib.base.type import ConfigType


class HeaderSetting(metaclass=ABCMeta):
    @abstractmethod
    def format_header(self, username: str) -> str:  # pragma: no cover
        pass


class SummarySetting(metaclass=ABCMeta):
    @abstractmethod
    def format_summary(
        self, today: ConfigType, maximum: ConfigType, total: ConfigType, continuous: ConfigType
    ) -> str:  # pragma: no cover
        pass


class GraphSetting(metaclass=ABCMeta):
    @abstractmethod
    def config_graph(self) -> ConfigType:  # pragma: no cover
        pass


class BaseLanguageSetting(HeaderSetting, SummarySetting, GraphSetting, metaclass=ABCMeta):
    pass
