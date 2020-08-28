from lib.base.type import ConfigType
from lib.language.base import BaseLanguageSetting
from lib.section.base import BaseSectionGenerator


class HeaderGenerator(BaseSectionGenerator):
    def __init__(self, username: str, setting: BaseLanguageSetting) -> None:
        self.username = username
        self.setting = setting

    def configure(self) -> ConfigType:
        return {
            "username": self.username,
        }

    def process(self, config: ConfigType) -> str:
        return self.setting.format_header(config=config)
