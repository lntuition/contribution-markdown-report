import os
import shutil
import subprocess
from unittest.mock import MagicMock

import pytest

from directory import change_workdir
from repository import Repository, RepositoryURL


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

    with change_workdir(repo.workdir):
        assert capture_stdout(["git", "rev-parse", "--abbrev-ref", "HEAD"]) == "master"


def test_repository_choose_branch(mock_repository_url, base_path):
    test_branch = "develop"

    repo = Repository(url=mock_repository_url, path=base_path, branch=test_branch)

    with change_workdir(repo.workdir):
        assert capture_stdout(["git", "rev-parse", "--abbrev-ref", "HEAD"]) == test_branch


def test_repository_configure(mock_repository_url, base_path):
    test_email = "email"
    test_name = "name"

    repo = Repository(url=mock_repository_url, path=base_path)
    repo.configure(email=test_email, name=test_name)

    with change_workdir(repo.workdir):
        assert capture_stdout(["git", "config", "--get", "user.email"]) == test_email
        assert capture_stdout(["git", "config", "--get", "user.name"]) == test_name


def test_repository_add(mock_repository_url, base_path):
    test_file = "touch"

    repo = Repository(url=mock_repository_url, path=base_path)

    with change_workdir(repo.workdir):
        open(test_file, "w").close()
        repo.add(path=test_file)

        assert capture_stdout(["git", "diff", "--name-only", "--cached"]) == test_file


def test_repository_commit(mock_repository_url, base_path):
    test_file = "touch"
    test_message = "message"

    repo = Repository(url=mock_repository_url, path=base_path)

    with change_workdir(repo.workdir):
        open(test_file, "w").close()
        repo.add(path=test_file)
        repo.commit(msg=test_message)

        assert capture_stdout(["git", "log", "--oneline", "-1"]).endswith(test_message)
