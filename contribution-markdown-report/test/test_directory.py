import os

import pytest

from directory import change_workdir


@pytest.fixture()
def cleanup_dir():
    def _cleanup_dir(path):
        os.removedirs(path)

    yield _cleanup_dir


@pytest.mark.parametrize(
    "workdir",
    [
        "relative_test_path",
        "/absolute/test/path",
    ],
    ids=[
        "Relative",
        "Absolute",
    ],
)
def test_change_workdir(workdir, cleanup_dir):
    current_workdir = os.getcwd()
    expected_workdir = os.path.join(current_workdir, workdir)

    with change_workdir(workdir):
        changed_workdir = os.getcwd()
        assert changed_workdir == expected_workdir

    assert current_workdir == os.getcwd()

    cleanup_dir(changed_workdir)
