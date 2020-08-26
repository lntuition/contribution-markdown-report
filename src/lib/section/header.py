from lib.base.type import ConfigType
from lib.language.base import LanguageSetting
from lib.section.base import SectionGenerator


class HeaderGenerator(SectionGenerator):
    def __init__(self, username: str, setting: LanguageSetting) -> None:
        self.username = username
        self.setting = setting

    def configure(self) -> ConfigType:
        return {
            "username": self.username,
        }

    def process(self, config: ConfigType) -> str:
        return self.setting.format_header(config=config)
