from abc import ABCMeta, abstractmethod

from lib.base.type import ConfigType


class BaseSectionGenerator(metaclass=ABCMeta):
    @abstractmethod
    def configure(self) -> ConfigType:  # pragma: no cover
        pass

    @abstractmethod
    def process(self, config: ConfigType) -> str:  # pragma: no cover
        pass

    def generate(self) -> str:
        return self.process(
            config=self.configure()
        )
