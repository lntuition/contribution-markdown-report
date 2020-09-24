import os

from git import Actor, Repo


class RepositoryURL:
    def __init__(self, user: str, token: str, name: str) -> None:
        self.__remote = f"https://{user}:{token}@github.com/{name}.git"

    @property
    def remote(self) -> str:
        return self.__remote


class Repository:
    def __init__(self, url: RepositoryURL, path: str, **kwargs) -> None:
        self.__repo = Repo.clone_from(url.remote, os.path.join(path, "target"), **kwargs)

    @property
    def workdir(self) -> str:
        return self.__repo.working_tree_dir

    def add(self, path: str) -> None:
        self.__repo.index.add(path)

    def commit(self, msg: str, name: str, email: str) -> None:
        if self.__repo.index.diff("HEAD"):
            config = Actor(name, email)
            self.__repo.index.commit(msg, author=config, committer=config)

    def push(self) -> None:
        self.__repo.remotes.origin.push()
