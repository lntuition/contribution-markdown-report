from abc import ABCMeta, abstractmethod

from lib.base.type import ConfigType


class BaseSectionGenerator(metaclass=ABCMeta):
    @abstractmethod
    def generate(self) -> str:  # pragma: no cover
        pass
