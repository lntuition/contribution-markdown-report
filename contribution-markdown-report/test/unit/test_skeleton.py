import pytest

from src.skeleton import MessageSkeleton


@pytest.mark.parametrize(
    "language",
    ["english"],
)
def test_get_skeleton(language: str) -> None:
    skeleton = MessageSkeleton.get_skeleton(language)

    assert skeleton == MessageSkeleton.skeleton[language]


def test_get_skeleton_with_warning() -> None:
    with pytest.warns(UserWarning):
        skeleton = MessageSkeleton.get_skeleton("NOTSUPPORTED")

    assert skeleton == MessageSkeleton.skeleton["english"]
