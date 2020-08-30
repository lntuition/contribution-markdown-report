from lib.language.base import BaseLanguageSetting
from lib.language.english import EnglishSetting


class NotSupportedException(Exception):
    pass


class FactoryLanguageSetting():
    def create_setting(self, language: str) -> BaseLanguageSetting:
        if language == "english":
            return EnglishSetting()
        else:
            raise NotSupportedException
