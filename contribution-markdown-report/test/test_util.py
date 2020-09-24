import os

import pytest

from util import EnvironException, safe_environ


@pytest.fixture
def base_key_value():
    key = "test_key"
    value = "test_value"

    os.environ[key] = value

    yield key, value

    del os.environ[key]


def test_safe_environ_default_success(base_key_value):
    key, value = base_key_value

    assert safe_environ(key) == value


def test_safe_environ_optional_success(base_key_value):
    key, value = base_key_value

    assert safe_environ(key, not_exist_ok=True) == value


def test_safe_environ_default_fail():
    with pytest.raises(EnvironException):
        safe_environ("will_never_exist_key")


def test_safe_environ_optional_fail():
    assert safe_environ("will_never_exist_key", not_exist_ok=True) == None
