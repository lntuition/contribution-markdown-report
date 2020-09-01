from lib.language.base import LanguageSetting
from lib.language.english import EnglishSetting


class NotSupportedException(Exception):
    pass


class FactoryLanguageSetting():
    def get_setting(self, language: str) -> LanguageSetting:
        if language == "english":
            return EnglishSetting()
        else:
            raise NotSupportedException
