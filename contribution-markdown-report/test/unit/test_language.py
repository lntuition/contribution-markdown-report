from typing import Type

import pytest

from src.language import LanguageSetting, LanguageSettingFactory


class TestLanguageSettingFactory:
    @pytest.mark.parametrize(
        ("language", "setting_type"),
        [
            ("english", LanguageSetting),
        ],
        ids=[
            "ENG",
        ],
    )
    def test_create(self, language: str, setting_type: Type[LanguageSetting]) -> None:
        setting = LanguageSettingFactory.create_setting(language=language)

        assert isinstance(setting, setting_type)

    def test_create_with_warning(self) -> None:
        with pytest.warns(UserWarning) as warn:
            setting = LanguageSettingFactory.create_setting(language="not supported")

        assert len(warn) == 1
        assert isinstance(setting, LanguageSetting)
