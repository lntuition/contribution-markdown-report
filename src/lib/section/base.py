from abc import ABCMeta, abstractmethod

from lib.language.base import LanguageSetting


class SectionGenerator(metaclass=ABCMeta):
    def __init__(self, setting: LanguageSetting) -> None:
        self.setting = setting

    @abstractmethod
    def generate(self) -> str:
        pass
