from abc import ABCMeta, abstractmethod
from typing import Any

from lib.language.base import LanguageSetting


class SectionGenerator(metaclass=ABCMeta):
    def __init__(self, setting: LanguageSetting) -> None:
        self.setting = setting

    @staticmethod
    def _bold_markdown(msg: Any) -> str:
        return f"**{msg}**"

    @staticmethod
    def _image_markdown(path: str) -> str:
        return f"![]({path})"

    @abstractmethod
    def generate(self) -> str:
        pass
