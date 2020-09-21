import pytest

from language.english import EnglishSetting
from language.factory import FactoryLanguageSetting, NotSupportedException


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
    ],
)
def test_get_setting(factory, language, expected_type):
    setting = factory.get_setting(language=language)

    assert isinstance(setting, expected_type)


def test_not_supported_create_setting(factory):
    with pytest.raises(NotSupportedException):
        factory.get_setting(language="not supported")
