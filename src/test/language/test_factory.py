import pytest

from lib.language.factory import FactoryLanguageSetting, NotSupportedException
from lib.language.english import EnglishSetting


@pytest.fixture(scope="module")
def factory():
    return FactoryLanguageSetting()


@pytest.mark.parametrize(
    ("language", "expected_type"),
    [
        ("english", EnglishSetting),
    ],
    ids=[
        "English",
    ]
)
def test_create_setting(factory, language, expected_type):
    setting = factory.create_setting(language=language)

    assert isinstance(setting, expected_type)


def test_not_supported_create_setting(factory):
    with pytest.raises(NotSupportedException):
        factory.create_setting(language="not supported")
