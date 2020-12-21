import pytest

from src.skeleton import SkeletonFactory


@pytest.mark.parametrize("language", ["english"])
def test_get_skeleton(language: str) -> None:
    skeleton = SkeletonFactory.get_skeleton(language)

    assert skeleton == SkeletonFactory._SkeletonFactory__skeleton[language]


def test_get_skeleton_with_warning() -> None:
    with pytest.warns(UserWarning):
        skeleton = SkeletonFactory.get_skeleton("NOTSUPPORTED")

    assert skeleton == SkeletonFactory._SkeletonFactory__skeleton["english"]
