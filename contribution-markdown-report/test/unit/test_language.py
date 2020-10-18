from typing import Type

import pytest

from src.language import BaseLanguageSetting, EnglishSetting, LanguageSettingFactory


class TestLanguageSettingFactory:
    @pytest.mark.parametrize(
        ("language", "expected"),
        [
            ("english", EnglishSetting),
        ],
        ids=[
            "ENG",
        ],
    )
    def test_create(self, language: str, expected: Type[BaseLanguageSetting]) -> None:
        created = LanguageSettingFactory.create_setting(language=language)

        assert created == expected

    def test_create_with_warning(self) -> None:
        with pytest.warns(UserWarning) as warn:
            setting = LanguageSettingFactory.create_setting(language="not supported")

        assert len(warn) == 1
        assert setting == EnglishSetting
