from lib.base.type import ConfigType
from lib.language.base import BaseLanguageSetting
from lib.section.base import BaseSectionGenerator


class HeaderGenerator(BaseSectionGenerator):
    def __init__(self, username: str, setting: BaseLanguageSetting) -> None:
        self.username = username
        self.setting = setting

    def generate(self) -> str:
        return self.setting.format_header(
            username=self.username
        )
