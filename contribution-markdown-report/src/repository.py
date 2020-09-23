import os

from git import Repo


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

    def configure(self, email: str, name: str) -> None:
        with self.__repo.config_writer() as config:
            config.set_value("user", "email", email)
            config.set_value("user", "name", name)

    def add(self, path: str) -> None:
        self.__repo.index.add(path)

    def commit(self, msg: str) -> None:
        self.__repo.index.commit(msg)

    def push(self) -> None:
        self.__repo.remotes.origin.push()
