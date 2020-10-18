import os
from contextlib import contextmanager
from typing import Iterator

import git

from .report import Report


class RepositoryActorBuilder:
    @staticmethod
    def build(name: str, email: str) -> git.Actor:
        return git.Actor(name, email)


class RepositoryCoreBuilder:
    @staticmethod
    def build(user: str, token: str, repository: str, branch: str) -> git.Repo:
        remote = f"https://{user}:{token}@github.com/{repository}.git"

        if branch != "":
            return git.Repo.clone_from(remote, "0781f0", branch=branch)

        return git.Repo.clone_from(remote, "0781f0")


class Repository:
    def __init__(self, core: git.Repo, actor: git.Actor, work_dir: str) -> None:
        if os.path.isabs(work_dir):
            raise Exception(f"{work_dir} : Cannot use absolute workdir")

        for path in os.path.split(work_dir):
            if path.startswith("..") or path.endswith(".."):
                raise Exception(f"{work_dir} : Cannot use '..' to workdir")

        self.__core = core
        self.__actor = actor
        self.__work_dir = work_dir

    @contextmanager
    def __change_workdir(self) -> Iterator[None]:
        cur_dir = os.getcwd()
        work_dir = os.path.join(
            self.__core.working_tree_dir,
            self.__work_dir,
        )

        os.makedirs(work_dir, exist_ok=True)
        os.chdir(work_dir)

        try:
            yield
        finally:
            os.chdir(cur_dir)

    def generate(self, report: Report) -> None:
        with self.__change_workdir():
            report.generate()

    def add(self) -> None:
        self.__core.index.add(self.__work_dir)

    def commit(self, report: Report) -> None:
        if self.__core.index.diff("HEAD"):
            msg = report.attribute(key="brief")
            self.__core.index.commit(msg, author=self.__actor, committer=self.__actor)

    def push(self) -> None:
        self.__core.remotes.origin.push()
