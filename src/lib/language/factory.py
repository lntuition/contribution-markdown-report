from lib.language.base import BaseLanguageSetting
from lib.language.english import EnglishSetting


class FactoryLanguageSetting():
    def create_setting(self, language: str) -> BaseLanguageSetting:
        language = language.lower()

        if language == "english" or language == "en":
            return EnglishSetting()
