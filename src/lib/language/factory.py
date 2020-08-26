from lib.language.base import LanguageSetting
from lib.language.english import EnglishSetting


class FactoryLanguageSetting():
    def create_setting(self, language: str) -> LanguageSetting:
        language = language.lower()

        if language == "english" or language == "en":
            return EnglishSetting()
