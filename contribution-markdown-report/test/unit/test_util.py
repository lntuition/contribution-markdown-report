import os

import pytest

from src.util import change_path


@pytest.mark.usefixtures("use_temporary_path")
def test_change_path() -> None:
    home = os.getcwd()

    with change_path("DESTINATION"):
        assert os.getcwd() == os.path.join(home, "DESTINATION")

    assert os.getcwd() == home
