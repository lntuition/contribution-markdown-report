from language.base import LanguageSetting
from language.english import EnglishSetting


class NotSupportedException(Exception):
    pass


def language_setting_factory(language: str) -> LanguageSetting:
    if language == "english":
        return EnglishSetting()

    raise NotSupportedException()
