import os
from typing import Optional


class EnvironException(Exception):
    pass


def safe_environ(key: str, not_exist_ok: bool = False) -> Optional[str]:
    value = os.environ.get(key, None)
    if not not_exist_ok and not value:
        raise EnvironException(f"[{key}] not exist")

    return value
