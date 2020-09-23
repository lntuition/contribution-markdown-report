import os

from git import Repo


class RepositoryURL():
    def __init__(self, user: str, token: str, name: str) -> None:
        self.__remote = f"https://{user}:{token}@github.com/{name}.git"

    @property
    def remote(self) -> str:
        return self.__remote


class RepositoryDir():
    def __init__(self, home: str, target: str) -> None:
        self.__base = os.path.join(home, "repo")
        self.__target = os.path.join(self.__base, target)

    @property
    def base(self) -> str:
        return self.__base

    @property
    def target(self) -> str:
        return self.__target


class RepositoryConfig():
    def __init__(self, email: str, name: str) -> None:
        self.__email = email
        self.__name = name

    def apply(self, repo: Repo) -> None:
        config = repo.config_writer()
        config.set_value("user", "email", self.__email)
        config.set_value("user", "name", self.__name)
        config.release()


class Repository:
    def __init__(
        self,
        url: RepositoryURL,
        workdir: RepositoryDir,
        config: RepositoryConfig,
        **kwargs
    ) -> None:
        self.__repo = Repo.clone_from(url.remote, workdir.base, **kwargs)
        self.__target = workdir.target
        config.apply(self.__repo)

    def add(self) -> None:
        self.__repo.index.add(self.__target)

    def commit(self, msg: str) -> None:
        self.__repo.index.commit(msg)

    def push(self) -> None:
        self.__repo.remotes.origin.push()
