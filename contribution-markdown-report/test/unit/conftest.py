import os
import shutil
from typing import Dict, Iterator
from unittest.mock import patch
from uuid import uuid4

import pytest


@pytest.fixture
def use_temporary_path() -> Iterator[None]:
    temporary_uuid = uuid4()
    temporary_path = os.path.join(
        os.path.abspath(os.sep),
        str(temporary_uuid),
    )
    recover_path = os.getcwd()

    try:
        os.makedirs(temporary_path)
        os.chdir(temporary_path)
        yield
    finally:
        shutil.rmtree(temporary_path)
        os.chdir(recover_path)


def __wrapper_fetch_text(url: str, params: Dict[str, str]) -> str:
    # Redirect fetch text to snapshot
    snapshot_path = os.path.join(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__),
            )
        ),
        "asset",
        params["from"][:4] + "_snapshot.html",
    )

    with open(snapshot_path, "r") as snapshot:
        return snapshot.read()


@pytest.fixture
def use_snapshot() -> Iterator[None]:
    with patch("src.request.Request.fetch_text", wraps=__wrapper_fetch_text):
        yield
