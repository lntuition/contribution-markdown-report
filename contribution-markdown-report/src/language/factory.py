from language.base import LanguageSetting
from language.english import EnglishSetting


class NotSupportedException(Exception):
    pass


class FactoryLanguageSetting:
    @staticmethod
    def get_setting(language: str) -> LanguageSetting:
        if language == "english":
            return EnglishSetting()

        raise NotSupportedException()
