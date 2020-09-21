import os
from contextlib import contextmanager
from typing import Iterator


@contextmanager
def change_workdir(workdir: str) -> Iterator[None]:
    prev_workdir = os.getcwd()
    os.makedirs(workdir, exist_ok=True)

    try:
        os.chdir(workdir)
        yield
    finally:
        os.chdir(prev_workdir)
