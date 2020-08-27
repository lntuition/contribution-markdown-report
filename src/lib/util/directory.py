import os
from contextlib import contextmanager


@contextmanager
def change_workdir(workdir: str) -> None:
    prev_workdir = os.getcwd()
    os.makedirs(workdir, exist_ok=True)

    try:
        os.chdir(workdir)
        yield
    finally:
        os.chdir(prev_workdir)
