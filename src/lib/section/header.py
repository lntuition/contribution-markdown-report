from lib.base.type import ConfigType
from lib.language.base import LanguageSetting
from lib.section.base import SectionGenerator


class HeaderGenerator(SectionGenerator):
    def __init__(self, username: str, setting: LanguageSetting) -> None:
        super().__init__(setting=setting)
        self.username = username

    def generate(self) -> str:
        return self.setting.format_header(
            username=self.username
        )
