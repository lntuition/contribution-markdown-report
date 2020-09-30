import pytest

from setting import (
    EnglishGraphSetting,
    EnglishHeaderSetting,
    EnglishSummarySetting,
    SettingFactory,
    SettingUnsupportedException,
)


@pytest.mark.parametrize(
    ("language", "settings_type"),
    [
        ("english", [EnglishHeaderSetting, EnglishSummarySetting, EnglishGraphSetting]),
    ],
    ids=[
        "English",
    ],
)
def test_setting_factory_create(language, settings_type):
    settings = SettingFactory.create_settings(language=language)

    for setting in settings:
        for setting_type in settings_type:
            if isinstance(setting, setting_type):
                break
        else:
            assert False


def test_setting_factory_unsupported():
    with pytest.raises(SettingUnsupportedException):
        SettingFactory.create_settings(language="unsupported")
