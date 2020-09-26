import os
import shutil
import subprocess
from unittest.mock import MagicMock

import pytest

from repository import Repository, RepositoryURL
from util import safe_chdir


def test_repository_url_remote():
    url = RepositoryURL(user="user", token="token", name="name")

    assert url.remote == f"https://user:token@github.com/name.git"


@pytest.fixture(scope="module")
def mock_repository_url():
    mock = MagicMock()
    mock.remote = "https://github.com/lntuition/contribution-markdown-report.git"
    return mock


@pytest.fixture()
def base_path():
    path = "/repository/test"
    os.makedirs(path, exist_ok=True)

    yield path

    shutil.rmtree(path, ignore_errors=True)


def test_repository_workdir(mock_repository_url, base_path):
    repo = Repository(url=mock_repository_url, path=base_path)

    assert repo.workdir.startswith(base_path)


def capture_stdout(cmd):
    return subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode("utf-8").strip()


def test_repository_default_branch(mock_repository_url, base_path):
    repo = Repository(url=mock_repository_url, path=base_path)

    with safe_chdir(repo.workdir):
        assert capture_stdout(["git", "rev-parse", "--abbrev-ref", "HEAD"]) == "master"


def test_repository_choose_branch(mock_repository_url, base_path):
    test_branch = "develop"

    repo = Repository(url=mock_repository_url, path=base_path, branch=test_branch)

    with safe_chdir(repo.workdir):
        assert capture_stdout(["git", "rev-parse", "--abbrev-ref", "HEAD"]) == test_branch


def test_repository_add(mock_repository_url, base_path):
    test_file = "touch"

    repo = Repository(url=mock_repository_url, path=base_path)

    with safe_chdir(repo.workdir):
        open(test_file, "w").close()
        repo.add(path=test_file)

        assert capture_stdout(["git", "diff", "--name-only", "--cached"]) == test_file


def test_repository_empty_add(mock_repository_url, base_path):
    repo = Repository(url=mock_repository_url, path=base_path)

    with safe_chdir(repo.workdir):
        repo.add(path=".gitignore")

        assert capture_stdout(["git", "diff", "--name-only", "--cached"]) == ""


def test_repository_commit(mock_repository_url, base_path):
    test_file = "touch"
    test_message = "message"
    test_name = "name"
    test_email = "email"

    repo = Repository(url=mock_repository_url, path=base_path)

    with safe_chdir(repo.workdir):
        open(test_file, "w").close()
        repo.add(path=test_file)
        repo.commit(msg=test_message, name=test_name, email=test_email)

        assert capture_stdout(["git", "log", "-1", "--format=%s"]) == test_message
        assert capture_stdout(["git", "log", "-1", "--format=%an"]) == test_name
        assert capture_stdout(["git", "log", "-1", "--format=%ae"]) == test_email


def test_repository_empty_commit(mock_repository_url, base_path):
    test_message = "message"
    test_name = "name"
    test_email = "email"

    repo = Repository(url=mock_repository_url, path=base_path)

    with safe_chdir(repo.workdir):
        head_message = capture_stdout(["git", "log", "-1", "--format=%s"])
        head_name = capture_stdout(["git", "log", "-1", "--format=%an"])
        head_email = capture_stdout(["git", "log", "-1", "--format=%ae"])

        repo.commit(msg=test_message, name=test_name, email=test_email)

        assert capture_stdout(["git", "log", "-1", "--format=%s"]) == head_message
        assert capture_stdout(["git", "log", "-1", "--format=%an"]) == head_name
        assert capture_stdout(["git", "log", "-1", "--format=%ae"]) == head_email
