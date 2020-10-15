import os
import shutil
import sys
from typing import Iterator

import pytest
import requests


def server_status() -> bool:
    if os.environ.get("DEBUG_FORCE_DEAD", False):
        return False

    try:
        response = requests.get("https://github.com")
        response.raise_for_status()
    except requests.RequestException:
        return False

    return True


server_ready = server_status()


@pytest.fixture
def live_server() -> None:
    if not server_ready:
        pytest.skip("Error at github server, skip live test")


@pytest.fixture
def dead_server() -> None:
    if server_ready:
        pytest.skip("No error at github server, skip dead test")


@pytest.fixture
def fake_root() -> Iterator[None]:
    cur_dir = os.getcwd()
    root = "/3921ab/root"

    os.makedirs(root)
    os.chdir(root)

    try:
        yield
    finally:
        shutil.rmtree(root)
        os.chdir(cur_dir)
