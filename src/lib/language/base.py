from abc import ABCMeta, abstractmethod

from lib.base.type import ConfigType


class BaseLanguageSetting(metaclass=ABCMeta):
    @abstractmethod
    def format_header(self, config: ConfigType) -> str:  # pragma: no cover
        pass

    @abstractmethod
    def format_summary(self, config: ConfigType) -> str:  # pragma: no cover
        pass

    @abstractmethod
    def config_graph(self) -> ConfigType:  # pragma: no cover
        pass
