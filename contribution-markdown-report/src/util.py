import contextlib
import os
from typing import Iterator


@contextlib.contextmanager
def change_path(dest: str) -> Iterator[None]:
    src = os.getcwd()

    try:
        os.makedirs(dest, exist_ok=True)
        os.chdir(dest)
        yield
    finally:
        os.chdir(src)
