import os
import shutil
from typing import Iterator
from unittest.mock import MagicMock, patch

import git
import pytest

from src.report import Report
from src.repository import Repository, RepositoryActorBuilder, RepositoryCoreBuilder


class FakeReport(Report):
    def __init__(self) -> None:
        self.__generate_directory = os.getcwd()
        self.__attribute = {
            "brief": "3629ab",
        }

    @property
    def generate_directory(self) -> str:
        return self.__generate_directory

    def attribute(self, key: str) -> str:
        return self.__attribute[key]

    def header_heading(self) -> str:
        return "header"

    def summary_heading(self) -> str:
        return "summary"

    def graph_heading(self) -> str:
        return "graph"

    def generate(self) -> None:
        self.__generate_directory = os.getcwd()


@pytest.fixture
def fake_core() -> Iterator[git.Repo]:
    path = "/81fa70/test-repository.git"

    try:
        yield git.Repo.init(path=path, mkdir=True)
    finally:
        shutil.rmtree(path)


@pytest.fixture
def fake_actor() -> git.Actor:
    return git.Actor("f98c10", "b302a1")


@pytest.fixture
def fake_report() -> FakeReport:
    return FakeReport()


class TestRepositoryActorBuilder:
    def test_build(self) -> None:
        name = "name"
        email = "email"

        assert git.Actor(name, email) == RepositoryActorBuilder.build(name=name, email=email)


class TestRepositoryCoreBuilder:
    @patch("git.Repo.clone_from")
    def test_default_branch(self, patch_repo_clone_from: MagicMock) -> None:
        user = "user"
        token = "token"
        repository = "repository"

        RepositoryCoreBuilder.build(user=user, token=token, repository=repository, branch="")
        call_args = patch_repo_clone_from.call_args

        assert f"https://{user}:{token}@github.com/{repository}.git" in call_args.args
        assert "branch" not in call_args.kwargs

    @pytest.mark.usefixtures("live_server")
    @pytest.mark.usefixtures("fake_root")
    def test_live_default_branch(self) -> None:
        core = RepositoryCoreBuilder.build(
            user="lntuition", token="", repository="lntuition/contribution-markdown-report", branch=""
        )

        assert core.active_branch.name == "master"

    @patch("git.Repo.clone_from")
    def test_choose_branch(self, patch_repo_clone_from: MagicMock) -> None:
        user = "user"
        token = "token"
        repository = "repository"
        branch = "develop"

        RepositoryCoreBuilder.build(user=user, token=token, repository=repository, branch=branch)
        call_args = patch_repo_clone_from.call_args

        assert f"https://{user}:{token}@github.com/{repository}.git" in call_args.args
        assert "branch" in call_args.kwargs
        assert branch == call_args.kwargs["branch"]

    @pytest.mark.usefixtures("live_server")
    @pytest.mark.usefixtures("fake_root")
    def test_live_choose_branch(self) -> None:
        branch = "develop"

        core = RepositoryCoreBuilder.build(
            user="lntuition", token="", repository="lntuition/contribution-markdown-report", branch=branch
        )

        assert core.active_branch.name == branch

    @pytest.mark.usefixtures("live_server")
    @pytest.mark.usefixtures("fake_root")
    def test_live_not_exist_branch(self) -> None:
        with pytest.raises(Exception):
            RepositoryCoreBuilder.build(
                user="lntuition", token="", repository="lntuition/contribution-markdown-report", branch="notexist"
            )


class TestRepository:
    @pytest.mark.parametrize(
        ("work_dir"),
        [
            "/absolute",
            "relative/../path",
        ],
        ids=[
            "Absolute",
            "..",
        ],
    )
    def test_wrong_work_dir(self, fake_core: git.Repo, fake_actor: git.Actor, work_dir: str) -> None:
        with pytest.raises(Exception):
            Repository(core=fake_core, actor=fake_actor, work_dir=work_dir)

    @pytest.mark.parametrize(
        ("work_dir"),
        [
            "",
            "relative",
            "relative/path",
            ".",
            "./relative",
            "./relative/path",
        ],
        ids=[
            "Implicit:depth:0",
            "Implicit:depth:1",
            "Implicit:depth:2",
            "Explicit:depth:0",
            "Explicit:depth:1",
            "Explicit:depth:2",
        ],
    )
    def test_generate(self, fake_core: git.Repo, fake_actor: git.Actor, work_dir: str, fake_report: FakeReport) -> None:
        generate_directory = os.path.join(fake_core.working_tree_dir, work_dir)

        repo = Repository(core=fake_core, actor=fake_actor, work_dir=work_dir)
        repo.generate(report=fake_report)

        assert os.path.samefile(generate_directory, fake_report.generate_directory)

    def test_add(self, fake_actor: git.Actor) -> None:
        mock_core = MagicMock()
        work_dir = "test/directory"

        repo = Repository(core=mock_core, actor=fake_actor, work_dir=work_dir)
        repo.add()

        mock_core.index.add.assert_called_with(work_dir)

    def test_commit(self, fake_actor: git.Actor, fake_report: FakeReport) -> None:
        mock_core = MagicMock()
        mock_core.index.diff.return_value = True

        msg = fake_report.attribute("brief")

        repo = Repository(core=mock_core, actor=fake_actor, work_dir="")
        repo.commit(report=fake_report)

        mock_core.index.commit.assert_called_with(
            msg,
            author=fake_actor,
            committer=fake_actor,
        )

    def test_push(self, fake_actor: git.Actor) -> None:
        mock_core = MagicMock()

        repo = Repository(core=mock_core, actor=fake_actor, work_dir="")
        repo.push()

        mock_core.remotes.origin.push.assert_called()
