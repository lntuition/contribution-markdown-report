import pytest

from language.english import EnglishSetting
from language.factory import NotSupportedException, language_setting_factory


@pytest.mark.parametrize(
    ("language", "expected_type"),
    [
        ("english", EnglishSetting),
    ],
    ids=[
        "English",
    ],
)
def test_language_setting_factory(language, expected_type):
    setting = language_setting_factory(language=language)

    assert isinstance(setting, expected_type)


def test_not_supported_language():
    with pytest.raises(NotSupportedException):
        language_setting_factory(language="not supported")
