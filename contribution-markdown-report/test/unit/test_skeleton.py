import pytest

from src.skeleton import SkeletonFactory


def test_default_language_with_warning() -> None:
    with pytest.warns(UserWarning):
        SkeletonFactory(language="NOTSUPPORTED")


@pytest.mark.parametrize("language", ["english"])
def test_get_string_map(language: str) -> None:
    string_map = SkeletonFactory(language=language).get_string_map()

    assert string_map == SkeletonFactory._SkeletonFactory__string_map[language]


@pytest.mark.parametrize("language", ["english"])
def test_get_list_map(language: str) -> None:
    list_map = SkeletonFactory(language=language).get_list_map()

    assert list_map == SkeletonFactory._SkeletonFactory__list_map[language]
