import os
from contextlib import contextmanager
from typing import Iterator, Optional


class EnvironException(Exception):
    pass


def safe_environ(key: str, not_exist_ok: bool = False) -> Optional[str]:
    value = os.environ.get(key, None)
    if not not_exist_ok and not value:
        raise EnvironException(f"[{key}] not exist")

    return value


@contextmanager
def safe_chdir(path: str) -> Iterator[None]:
    curdir = os.getcwd()
    os.makedirs(path, exist_ok=True)
    os.chdir(path)

    try:
        yield
    finally:
        os.chdir(curdir)
